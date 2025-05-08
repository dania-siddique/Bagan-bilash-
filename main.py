import sys
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from database import Base, engine

Base.metadata.create_all(bind=engine)
# Optional: Ensure project root is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import routers from features
from feature1.backend.main import router as feature1_router
from feature2.main import router as feature2_router
from feature3.main import router as feature3_router
from feature4.backend.main import router as feature4_router

app = FastAPI()

# Mount global static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Register feature routers with prefixes
app.include_router(feature1_router, prefix="/feature1")
app.include_router(feature2_router, prefix="/feature2")
app.include_router(feature3_router, prefix="/feature3")
app.include_router(feature4_router, prefix="/feature4")

# Homepage route
@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
