from fastapi import APIRouter, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json

router = APIRouter()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
frontend_dir = BASE_DIR / "frontend"
reminders_file = BASE_DIR / "backend" / "reminders.json"

templates = Jinja2Templates(directory=str(frontend_dir))

# Initialize reminders.json if it doesn't exist
if not reminders_file.exists():
    with open(reminders_file, "w") as f:
        json.dump([], f)

def load_reminders():
    if reminders_file.stat().st_size == 0:
        return []
    with open(reminders_file, "r") as f:
        return json.load(f)

def save_reminders(reminders):
    with open(reminders_file, "w") as f:
        json.dump(reminders, f, indent=2)

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/add-reminder/")
async def add_reminder(plant_name: str = Form(...), days: int = Form(...)):
    reminders = load_reminders()
    reminders.append({"plant": plant_name, "days": days})
    save_reminders(reminders)
    return {"message": f"Reminder set to water {plant_name} every {days} days"}

@router.get("/get-reminders/")
async def get_reminders():
    return load_reminders()
