from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, User, Plant, add_plants

# FastAPI app setup
app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Profile Update
@app.get("/", response_class=HTMLResponse)
async def profile_settings(request: Request, db: Session = Depends(get_db)):
    user = db.query(User).first()  # Get the first user (for simplicity)
    return templates.TemplateResponse("account.html", {"request": request, "user": user})

# andle profile update
@app.post("/update-profile", response_class=HTMLResponse)
async def update_profile(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).first()
    
    if not user:
        return RedirectResponse(url="/?message=User not found&message_type=error", status_code=303)

    user.name = name
    user.email = email
    if new_password:
        user.password = new_password  # Hashing can be added here if needed
    
    db.commit()
    return RedirectResponse(url="/?message=Profile updated successfully&message_type=success", status_code=303)

# Seller Interface (
@app.get("/seller", response_class=HTMLResponse)
async def seller_interface(request: Request, db: Session = Depends(get_db)):
    # Fetch success message from query parameter if any
    success_message = request.query_params.get('message', None)
    return templates.TemplateResponse("seller.html", {"request": request, "success_message": success_message})

#handle adding new plants (sekker)
@app.post("/add-plant", response_class=HTMLResponse)
async def add_plant(
    request: Request,
    plant_name: str = Form(...),
    plant_price: float = Form(...),
    db: Session = Depends(get_db)
):
   
    new_plant = Plant(name=plant_name, price=plant_price)
    db.add(new_plant)
    db.commit()

    
    return RedirectResponse(url="/seller?message=Plant+added+successfully", status_code=303)

# Buyer Interface
@app.get("/buyer", response_class=HTMLResponse)
async def buyer_interface(request: Request, db: Session = Depends(get_db)):
    plants = db.query(Plant).all()
    return templates.TemplateResponse("buyer.html", {"request": request, "plants": plants})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
