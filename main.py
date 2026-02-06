from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os

from services.pdf_engine import edit_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TMP = "tmp"
os.makedirs(TMP, exist_ok=True)


@app.post("/edit")
async def edit(
    file: UploadFile = File(...),
    edits: str = Form(...)
):
    uid = str(uuid.uuid4())
    input_path = f"{TMP}/{uid}.pdf"
    output_path = f"{TMP}/{uid}_out.pdf"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    edit_pdf(input_path, output_path, edits)

    return FileResponse(output_path, filename="edited.pdf")
