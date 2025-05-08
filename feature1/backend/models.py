from sqlalchemy import Column, Integer, String, LargeBinary
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    bio = Column(String, nullable=True)
    profile_picture = Column(LargeBinary, nullable=True)
    password_hash = Column(String)