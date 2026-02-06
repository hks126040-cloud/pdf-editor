from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid, os, shutil
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD = "uploads"
OUTPUT = "outputs"
os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)


@app.post("/edit-position")
async def edit_pdf(
    file: UploadFile = File(...),
    text: str = Form(...),
    x: float = Form(...),
    y: float = Form(...),
    page: int = Form(...)
):
    file_id = str(uuid.uuid4())

    input_path = f"{UPLOAD}/{file_id}.pdf"
    overlay_path = f"{UPLOAD}/{file_id}_overlay.pdf"
    output_path = f"{OUTPUT}/{file_id}.pdf"

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    # create overlay
    c = canvas.Canvas(overlay_path)
    c.drawString(x, y, text)
    c.save()

    overlay_pdf = PdfReader(overlay_path)

    for i, p in enumerate(reader.pages):
        if i == page:
            p.merge_page(overlay_pdf.pages[0])
        writer.add_page(p)

    with open(output_path, "wb") as f:
        writer.write(f)

    return FileResponse(output_path, media_type="application/pdf", filename="edited.pdf")
