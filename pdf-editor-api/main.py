from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
import os, uuid, shutil
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.post("/edit-position")
async def edit_position(
    file: UploadFile = File(...),
    page: int = Form(...),
    x: float = Form(...),
    y: float = Form(...),
    text: str = Form(...)
):
    try:
        file_id = str(uuid.uuid4())
        input_path = f"{UPLOAD_DIR}/{file_id}.pdf"
        output_path = f"{OUTPUT_DIR}/{file_id}.pdf"

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        reader = PdfReader(input_path)
        writer = PdfWriter()

        for i, p in enumerate(reader.pages):
            if i == page:
                packet_path = f"{UPLOAD_DIR}/{file_id}_overlay.pdf"
                c = canvas.Canvas(packet_path, pagesize=letter)
                c.drawString(x, y, text)
                c.save()

                overlay_reader = PdfReader(packet_path)
                p.merge_page(overlay_reader.pages[0])

            writer.add_page(p)

        with open(output_path, "wb") as f:
            writer.write(f)

        return FileResponse(output_path, media_type="application/pdf", filename="edited.pdf")

    except Exception as e:
        return {"error": str(e)}
