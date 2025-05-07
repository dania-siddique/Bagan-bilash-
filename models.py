# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base
from sqlalchemy import Float, DateTime
from datetime import datetime


class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(String(255))

class Participation(Base):
    __tablename__ = "participations"
    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    username = Column(String(100))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100))
    email = Column(String(100))
    is_admin = Column(Boolean)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(255))
    username = Column(String(100))  # Who posted it

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100))
    amount = Column(Float)
    status = Column(String(50))  # e.g. 'Pending', 'Completed', 'Failed'
    method = Column(String(50))  # e.g. 'bKash', 'Nagad', 'Card'
    timestamp = Column(DateTime, default=datetime.utcnow)
