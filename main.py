from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

# CORS ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kullanıcıdan yüz fotoğrafı al (demo - dosya kaydedilmiyor)
@app.post("/upload/")
async def upload_image(user_name: str = Form(...), file: UploadFile = File(...)):
    try:
        return JSONResponse(content={
            "message": "Fotoğraf yüklendi ve işleme hazır (kaydedilmedi - simülasyon).",
            "file_name": file.filename
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Morfran FaceSwap API çağrısı
@app.post("/faceswap/")
async def face_swap(request: Request):
    try:
        data = await request.json()
        source_url = data.get("source_url")  # Kullanıcının yüz görseli
        target_url = data.get("target_url")  # Sabit model görseli

        payload = {
            "SourceImageUrl": source_url,
            "TargetImageUrl": target_url,
            "MatchGender": True,
            "MaximumFaceSwapNumber": 1
        }

        headers = {
            "Content-Type": "application/json"
        }

        # Morfran FaceSwap API endpoint
        response = requests.post("https://api.morfran.com/faceswap", json=payload, headers=headers)
        return JSONResponse(status_code=response.status_code, content=response.json())

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def root():
    return {"message": "FaceSwap API çalışıyor!"}
