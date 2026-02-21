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
