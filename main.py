from fastapi import FastAPI, Form, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import random
from datetime import datetime
import shutil

app = FastAPI()

# Setup static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DB_FILE = "database.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Plant Swap tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS swap_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plant_name TEXT,
        price REAL,
        picture TEXT,
        want_to_swap_with TEXT,
        created_at TEXT
    )''')
    
    # Plant Donation tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS donations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donor_name TEXT NOT NULL,
        plant_type TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )''')
    
    conn.commit()
    conn.close()

init_db()

# Routes
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Plant Swap Feature
@app.get("/swap")
async def swap_page(request: Request):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM swap_requests ORDER BY created_at DESC")
    requests = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("swap.html", {"request": request, "requests": requests})

@app.post("/swap/add")
async def add_swap(
    plant_name: str = Form(...),
    price: float = Form(...),
    want_to_swap_with: str = Form(...),
    picture: UploadFile = File(...)
):
    upload_folder = "static/uploads"
    os.makedirs(upload_folder, exist_ok=True)
    picture_path = f"uploads/{picture.filename}"
    
    with open(f"static/{picture_path}", "wb") as f:
        shutil.copyfileobj(picture.file, f)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO swap_requests (plant_name, price, picture, want_to_swap_with, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (plant_name, price, picture_path, want_to_swap_with, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/swap", status_code=302)

# Plant Donation Feature
@app.get("/donate")
async def donate_page(request: Request):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donations ORDER BY id DESC")
    donations = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("donate.html", {"request": request, "donations": donations})

@app.post("/donate/add")
async def add_donation(
    donor_name: str = Form(...),
    plant_type: str = Form(...),
    quantity: int = Form(...)
):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO donations (donor_name, plant_type, quantity) VALUES (?, ?, ?)",
        (donor_name, plant_type, quantity)
    )
    conn.commit()
    conn.close()
    return RedirectResponse("/donate", status_code=303)

# Parcel Tracking Feature
current_location = {
    "lat": 23.8103,
    "lng": 90.4125,
    "timestamp": datetime.now().isoformat()
}

@app.get("/track")
async def track_page(request: Request):
    return templates.TemplateResponse("track.html", {"request": request})

@app.get("/location")
def get_location():
    # Simulate movement
    current_location["lat"] += random.uniform(-0.001, 0.001)
    current_location["lng"] += random.uniform(-0.001, 0.001)
    current_location["timestamp"] = datetime.now().isoformat()
    return current_location