# type: ignore
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP 
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(TIMESTAMP, default=datetime.now(datetime.timetz.utcnow))

    ideas = relationship("Idea", back_populates="owner")

class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    idea = Column(Text)
    submitted_at = Column(TIMESTAMP, default=datetime.now(datetime.timetz.utcnow))

    ai_validation_result = relationship("AIValidationResult", back_populates="idea")

class AIValidationResult(Base):
    __tablename__ = "ai_validation_results"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, index=True)
    market_demand = Column(String(50))
    competitors = Column(Text)
    pricing_strategy = Column(String(50))
    growth_potential = Column(String(50))
    ai_analysis = Column(Text)
    validated_at = Column(TIMESTAMP, default=datetime.now(datetime.timetz.utcnow))
