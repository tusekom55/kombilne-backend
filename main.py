from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import requests
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gerçekten dosya kaydedilen klasörü oluştur
UPLOAD_DIR = "uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Statik dosyaları servis et (model.jpg vs)
app.mount("/uploaded", StaticFiles(directory="uploaded"), name="uploaded")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Yüz fotoğrafı yükleme
@app.post("/upload/")
async def upload_image(user_name: str = Form(...), file: UploadFile = File(...)):
    try:
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())

        return JSONResponse(content={
            "message": "Fotoğraf yüklendi ve işleme hazır.",
            "file_name": file.filename
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Morfran ile yüz değiştirme
@app.post("/faceswap/")
async def face_swap(request: Request):
    try:
        data = await request.json()
        source_url = data.get("source_url")
        target_url = data.get("target_url")

        payload = {
            "SourceImageUrl": source_url,
            "TargetImageUrl": target_url,
            "MatchGender": True,
            "MaximumFaceSwapNumber": 1
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post("https://api.morfran.com/faceswap", json=payload, headers=headers)
        return JSONResponse(status_code=response.status_code, content=response.json())

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Root test
@app.get("/")
def root():
    return {"message": "FaceSwap API çalışıyor!"}
