from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(title="MousaviTax API Gateway", version="0.2.1")

# مسیر دقیق build Next.js (در ویندوز حتماً از / استفاده کنید)
NEXTJS_BUILD_DIR = Path(r"D:\AI\GitHub\mousavitax-platform\apps\web\build")

STATIC_NEXT_DIR = NEXTJS_BUILD_DIR / "_next/static"
STATIC_ASSETS_DIR = NEXTJS_BUILD_DIR / "assets"

# استاتیک Next.js
app.mount("/_next/static", StaticFiles(directory=STATIC_NEXT_DIR), name="next-static")
app.mount("/assets", StaticFiles(directory=STATIC_ASSETS_DIR), name="next-assets")

# برای همه مسیرها همیشه index.html بده (React Router کار کند)
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    return FileResponse(NEXTJS_BUILD_DIR / "index.html")

# متد خاص برای صفحه waiver
@app.get("/waiver")
async def waiver_page():
    return FileResponse(NEXTJS_BUILD_DIR / "index.html")
