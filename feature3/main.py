from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Dict
from pathlib import Path
import json
from feature3.models import User, Message

from database import SessionLocal  # Update to your actual structure
from datetime import datetime

router = APIRouter()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "frontend/templates")

# Active WebSocket connections
active_connections: Dict[str, WebSocket] = {}

@router.get("/", response_class=HTMLResponse)
async def user_page(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@router.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return templates.TemplateResponse("admin.html", {"request": request, "users": users})

@router.websocket("/ws/user/{user_id}")
async def user_websocket(websocket: WebSocket, user_id: str):
    await websocket.accept()
    active_connections[user_id] = websocket

    db = SessionLocal()
    if not db.query(User).filter_by(id=user_id).first():
        db.add(User(id=user_id))
        db.commit()

    try:
        while True:
            data = await websocket.receive_text()
            message = Message(sender_id=user_id, receiver_id="admin", content=data)
            db.add(message)
            db.commit()

            if "admin" in active_connections:
                await active_connections["admin"].send_text(json.dumps({
                    "type": "user_message",
                    "sender": user_id,
                    "text": data,
                    "time": message.timestamp.isoformat()
                }))
    except WebSocketDisconnect:
        del active_connections[user_id]
    finally:
        db.close()

@router.websocket("/ws/admin")
async def admin_websocket(websocket: WebSocket):
    await websocket.accept()
    active_connections["admin"] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        del active_connections["admin"]

@router.post("/admin/reply")
async def admin_reply(sender_id: str, content: str):
    db = SessionLocal()
    message = Message(sender_id="admin", receiver_id=sender_id, content=content)
    db.add(message)
    db.commit()

    if sender_id in active_connections:
        await active_connections[sender_id].send_text(json.dumps({
            "type": "admin_reply",
            "text": content,
            "time": message.timestamp.isoformat()
        }))
    db.close()
    return {"status": "sent"}
