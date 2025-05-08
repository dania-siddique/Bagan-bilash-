from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker, Session
from passlib.context import CryptContext

SQLALCHEMY_DATABASE_URL = "sqlite:///./baganbilash.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Plant(Base):
    __tablename__ = "plants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)



def add_plants(db: Session):
    plants = [
        {"name": "BaganBilash", "price": 120},
        {"name": "Rose", "price": 214},
        {"name": "Sunflower", "price": 163},
        {"name": "Tulip", "price": 210}
    ]
    
    for plant in plants:
        db_plant = db.query(Plant).filter(Plant.name == plant["name"]).first()
        if not db_plant:  
            db_plant = Plant(name=plant["name"], price=plant["price"])
            db.add(db_plant)
    
    db.commit()

# Drop all existing tables and recreate necessary ones (User and Plant)
Base.metadata.drop_all(bind=engine)  # Drops all tables, including the reviews table if it exists
Base.metadata.create_all(bind=engine)  # Recreates only the necessary tables (User, Plant)

print("Database reset complete!")

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")
