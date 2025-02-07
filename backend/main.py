# type: ignore
import openai 
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from pytrends.request import TrendReq
from sqlalchemy.orm import Session
from config.db import SessionLocal
from models import models
from config.redis import get_redis
import json


# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY") 

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# redis instance
@app.on_event("startup")
async def startup():
    global redis
    redis = await get_redis()

@app.on_event("shutdown")
async def shutdown():
    await redis.close()

class IdeaRequest(BaseModel):
    idea: str

# Fetch competitors using SerpAPI
async def get_competitors(idea: str):
    cached_competitors = await redis.get(f"competitors:{idea}")
    if cached_competitors:
        return json.loads(cached_competitors)
    try:
        search_url = os.getenv("SERPAPI_URL")
        params = {
            "q": f"{idea} competitors",
            "api_key": SERPAPI_KEY,
            "num": 5
        }
        response = requests.get(search_url, params=params)
        data = response.json()

        competitors = [result["title"] for result in data.get("organic_results", []) if "title" in result]

        # Cache competitors (set TTL for 24 hours)
        await redis.setex(f"competitors:{idea}", 86400, json.dumps(competitors))

        return competitors if competitors else ["No competitors found"]

    except Exception as e:
        return [f"Error fetching competitors: {str(e)}"]

# Fetch market demand using Google Trends API
async def get_market_demand(idea: str):
    cache_key = f"market_demand:{idea}"

    # check if market demand is already cached
    cached_demand = await redis.get(cache_key)
    if cached_demand:
        return cached_demand  

    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([idea], cat=0, timeframe='today 12-m')
        trends_data = pytrends.interest_over_time()

        if not trends_data.empty:
            avg_interest = trends_data[idea].mean()
            if avg_interest > 50:
                demand = "High Demand"
            elif avg_interest > 20:
                demand = "Moderate Demand"
            else:
                demand = "Low Demand"
        else:
            demand = "Market data unavailable"

        # cache the result for 12 hours
        await redis.setex(cache_key, 43200, demand)

        return demand

    except Exception as e:
        return f"Error fetching market demand: {str(e)}"

# API route to validate startup ideas
@app.post("/validate")
async def validate_idea(request: IdeaRequest, db: Session = Depends(get_db)):
    idea = request.idea
    
    # check if AI result is cached
    cached_result = await redis.get(f"ai_validation:{idea}")
    if cached_result:
        return json.loads(cached_result)
    try:
        competitors = await get_competitors(idea)
        market_demand = await get_market_demand(idea)
        # Check if user exists or create new user (for simplicity)
        user = db.query(models.User).filter(models.User.email == "fenil@gmail.com").first()
        if not user:
            user = models.User(name="Fenil Vaghasiya", email="fenil@gmail.com")
            db.add(user)
            db.commit()
            db.refresh(user)

        # Store the idea in the database
        new_idea = models.Idea(user_id=user.id, idea=idea)
        db.add(new_idea)
        db.commit()
        db.refresh(new_idea)

        # Call AI to validate the idea
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are an expert startup idea validator."},
                {"role": "user", "content": f"Validate this startup idea: {idea}. Provide key takeaways."}
            ],
            max_tokens=200
        )
        validation_result = response["choices"][0]["message"]["content"]

        # Store AI validation results
        ai_result = models.AIValidationResult(
        idea_id=new_idea.id,
        market_demand=market_demand,  
        competitors=competitors,      
        pricing_strategy="Premium",  
        growth_potential="Moderate",  
        ai_analysis=validation_result 
)
        db.add(ai_result)
        db.commit()
        db.refresh(ai_result)

        # cache AI result for 24 hours
        response_data = {
            "market_demand": market_demand,
            "competitors": competitors,
            "pricing_strategy": "Freemium",
            "growth_potential": "Moderate",
            "ai_analysis": validation_result
        }
        await redis.setex(f"ai_validation:{idea}", 86400, json.dumps(response_data))

        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))