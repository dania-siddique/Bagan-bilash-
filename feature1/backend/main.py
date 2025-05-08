from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pathlib import Path
import os

from feature1.backend import models
from feature1.backend import schemas  # Make sure this exists
from feature1.backend.database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Configure paths
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "frontend/templates")
static_dir = BASE_DIR / "frontend/static"

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_class=HTMLResponse)
async def get_profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@router.post("/users/")
def create_user(
    username: str = Form(...),
    bio: str = Form(None),
    password: str = Form(...),
    profile_picture: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    picture_data = None
    if profile_picture:
        picture_data = profile_picture.file.read()
    
    user = models.User(
        username=username,
        bio=bio,
        profile_picture=picture_data,
        password_hash=password  # In production, hash this
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return RedirectResponse(url=f"/feature1/profiles/{user.username}", status_code=303)

@router.get("/profiles/{username}", response_class=HTMLResponse)
async def profiles_page(request: Request, username: str, db: Session = Depends(get_db)):
    current_user = db.query(models.User).filter(models.User.username == username).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    other_users = db.query(models.User).filter(models.User.username != username).all()
    
    return templates.TemplateResponse("profiles.html", {
        "request": request,
        "current_user": current_user,
        "other_users": other_users
    })

@router.get("/profile-picture/{user_id}")
async def get_profile_picture(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or not user.profile_picture:
        return FileResponse(static_dir / "default-profile.png")
    return Response(content=user.profile_picture, media_type="image/jpeg")
