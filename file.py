from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount(
    "/uploads",
    StaticFiles(directory="/Project_2/uploads"),
    name="/uploads"
)

@app.post("/uploads")
async def upload_image(file: UploadFile = File(...)):
    with open(f"uploads/{file.filename}", "wb") as image:
        image.write(await file.read())
              
    return {
        "image_url": f"/uploads/{file.filename}"
    }