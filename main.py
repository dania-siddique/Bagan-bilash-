# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
from fastapi.templating import Jinja2Templates
from fastapi import Request

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "FastAPI Gardening App"}


@app.post("/challenges")
def create_challenge(challenge: schemas.ChallengeCreate, db: Session = Depends(get_db)):
    new_challenge = models.Challenge(
        title=challenge.title,
        description=challenge.description
    )
    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)
    return new_challenge


@app.post("/challenges/{challenge_id}/join")
def join_challenge(challenge_id: int, participation: schemas.ParticipationCreate, db: Session = Depends(get_db)):
    challenge = db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    join = models.Participation(
        challenge_id=challenge_id,
        username=participation.username
    )
    db.add(join)
    db.commit()
    return {"message": f"{participation.username} joined challenge '{challenge.title}'"}


@app.post("/posts")
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(
        title=post.title,
        description=post.description,
        username=post.username
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts", response_class=HTMLResponse)
def view_posts(request: Request, db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return templates.TemplateResponse("post_list.html", {
        "request": request,
        "posts": posts
    })


@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    posts = db.query(models.Post).all()
    challenges = db.query(models.Challenge).all()
    participations = db.query(models.Participation).all()
    return templates.TemplateResponse("admin_panel.html", {
        "request": request,
        "users": users,
        "posts": posts,
        "challenges": challenges,
        "participations": participations
    })

@app.post("/transactions")
def create_transaction(data: schemas.TransactionCreate, db: Session = Depends(get_db)):
    new_txn = models.Transaction(
        username=data.username,
        amount=data.amount,
        status="Pending",  # Default
        method=data.method
    )
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return new_txn


@app.get("/transactions/{username}")
def get_transactions(username: str, db: Session = Depends(get_db)):
    txns = db.query(models.Transaction).filter(models.Transaction.username == username).all()
    return txns

@app.get("/transactions/view", response_class=HTMLResponse)
def view_transactions(request: Request, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).all()
    return templates.TemplateResponse("transactions.html", {
        "request": request,
        "transactions": transactions
    })







#uvicorn main:app --reload

import os
print("Database path:", os.path.abspath("gardening.db"))



