from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).parent
WEBAPP_DIR = BASE_DIR / "webapp"

app = FastAPI()
app.mount("/webapp/static", StaticFiles(directory=WEBAPP_DIR), name="webapp-static")


@app.get("/api/ping")
async def ping() -> JSONResponse:
    return JSONResponse({"ok": True})


@app.get("/webapp")
async def webapp() -> FileResponse:
    return FileResponse(WEBAPP_DIR / "index.html")
from fastapi.responses import StreamingResponse
from reportlab.pdfgen import canvas
import io

@app.post("/api/render")
async def render_pdf(data: dict):
    text = data.get("text", "")

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, text)
    p.save()

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=output.pdf"}
    )
