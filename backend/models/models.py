# type: ignore
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey 
from sqlalchemy.orm import relationship
from datetime import datetime
from config.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(TIMESTAMP, default=datetime.now)

    # Relationship to Ideas (One-to-many: one User can have many Ideas)
    ideas = relationship("Idea", back_populates="owner")


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)  # Foreign Key referencing User
    idea = Column(Text)
    submitted_at = Column(TIMESTAMP, default=datetime.now)

    # Relationship to AIValidationResult (One-to-one: each Idea can have one AIValidationResult)
    ai_validation_result = relationship("AIValidationResult", back_populates="idea", uselist=False)

    # Relationship to User (Many-to-one: multiple Ideas can belong to one User)
    owner = relationship("User", back_populates="ideas")


class AIValidationResult(Base):
    __tablename__ = "ai_validation_results"

    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"), index=True)  # Foreign Key referencing Idea
    market_demand = Column(String(50))
    competitors = Column(Text)
    pricing_strategy = Column(String(50))
    growth_potential = Column(String(50))
    ai_analysis = Column(Text)
    validated_at = Column(TIMESTAMP, default=datetime.now)

    # Relationship to Idea (One-to-one: each AIValidationResult belongs to one Idea)
    idea = relationship("Idea", back_populates="ai_validation_result")