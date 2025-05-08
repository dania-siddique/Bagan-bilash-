from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import requests
import os

router = APIRouter()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "frontend/templates")

HF_API_KEY = os.getenv("HF_API_KEY", "your_hf_api_key_here")
MODEL_API_URL = "https://api-inference.huggingface.com/models/facebook/bart-large-cnn"

PLANT_DATABASE = {
    "tulip": { ... },  # Keep your plant dict as is
    "rose": { ... },
    "general": { ... }
}

async def get_plant_info(plant_name: str):
    plant_name = plant_name.strip().lower()
    if plant_name in PLANT_DATABASE:
        return {
            "success": True,
            "result": PLANT_DATABASE[plant_name]["summary"],
            "tips": PLANT_DATABASE[plant_name].get("tips", ""),
            "source": "local_database"
        }

    for name, data in PLANT_DATABASE.items():
        if name in plant_name or plant_name in name:
            return {
                "success": True,
                "result": data["summary"],
                "tips": data.get("tips", ""),
                "source": "local_fallback"
            }

    if HF_API_KEY.startswith("hf_"):
        try:
            prompt = f"""Provide detailed planting instructions for {plant_name}..."""
            response = requests.post(
                MODEL_API_URL,
                headers={"Authorization": f"Bearer {HF_API_KEY}"},
                json={"inputs": prompt},
                timeout=15
            )
            if response.status_code == 200:
                result = response.json()[0]['summary_text']
                return {
                    "success": True,
                    "result": result.replace('\n', '<br>'),
                    "source": "huggingface_api"
                }
        except Exception:
            pass

    return {
        "success": True,
        "result": PLANT_DATABASE["general"]["summary"],
        "tips": "While we don't have specific info for this plant...",
        "source": "general_fallback"
    }

@router.get("/how-to-plant", response_class=HTMLResponse)
async def how_to_plant(request: Request):
    return templates.TemplateResponse("how_to_plant.html", {"request": request})

@router.get("/plant-search")
async def plant_search(plant_name: str):
    if not plant_name.strip():
        return JSONResponse(
            status_code=400,
            content={"success": False, "error": "Please enter a plant name"}
        )
    plant_info = await get_plant_info(plant_name)
    return JSONResponse(content=plant_info)
