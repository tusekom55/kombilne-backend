from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS ayarı (herkese izin veriyoruz)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_image(user_name: str = Form(...), file: UploadFile = File(...)):
    try:
        # Render sunucusunda dosya yazmaya çalışmıyoruz.
        # Sadece yüklenen dosya ismini döndürüyoruz
        return JSONResponse(content={
            "message": "Fotoğraf yüklendi ve işleme hazır (kaydedilmedi - simülasyon).",
            "file_name": file.filename
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/")
def root():
    return {"message": "FaceSwap API çalışıyor!"}
