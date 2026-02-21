from fastapi import Query
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import os

def _register_multilang_font():
    # Самый универсальный шрифт для: RU / KZ / TJ / EN / TR
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont("MultiSans", path))
            return "MultiSans"

    # Если вдруг в окружении нет системных шрифтов — будет квадратиками,
    # но это случается редко на Render.
    return "Helvetica"

@app.get("/api/render")
async def render_pdf_get(
    text: str = Query(default="", max_length=20000),
    font_size: int = Query(default=14, ge=8, le=40),
    line_height: int = Query(default=18, ge=10, le=60),
):
    buffer = io.BytesIO()

    font_name = _register_multilang_font()

    # A4 + нормальные поля
    width, height = A4
    left = 15 * mm
    top = 15 * mm
    y = height - top

    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont(font_name, font_size)

    # Многострочный текст + перенос страниц
    for raw_line in (text or "").split("\n"):
        line = raw_line.rstrip("\r")
        # пустая строка
        if line == "":
            y -= line_height
        else:
            # очень простой перенос по ширине страницы (без "умного" переноса)
            # если хочешь — сделаем умный позже
            max_width = width - left - 15 * mm
            words = line.split(" ")
            current = ""
            for w in words:
                test = (current + " " + w).strip()
                if p.stringWidth(test, font_name, font_size) <= max_width:
                    current = test
                else:
                    # печатаем текущую строку
                    if y < 15 * mm:
                        p.showPage()
                        p.setFont(font_name, font_size)
                        y = height - top
                    p.drawString(left, y, current)
                    y -= line_height
                    current = w
            if current:
                if y < 15 * mm:
                    p.showPage()
                    p.setFont(font_name, font_size)
                    y = height - top
                p.drawString(left, y, current)
                y -= line_height

        # перенос страницы, если дошли до низа
        if y < 15 * mm:
            p.showPage()
            p.setFont(font_name, font_size)
            y = height - top

    p.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=output.pdf"}
    )
