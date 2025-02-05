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

class IdeaRequest(BaseModel):
    idea: str

# Fetch competitors using SerpAPI
def get_competitors(idea: str):
    try:
        search_url = "https://serpapi.com/search"
        params = {
            "q": f"{idea} competitors",
            "api_key": SERPAPI_KEY,
            "num": 5
        }
        response = requests.get(search_url, params=params)
        data = response.json()

        competitors = [result["title"] for result in data.get("organic_results", []) if "title" in result]
        return competitors if competitors else ["No competitors found"]

    except Exception as e:
        return [f"Error fetching competitors: {str(e)}"]

# Fetch market demand using Google Trends API
def get_market_demand(idea: str):
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([idea], cat=0, timeframe='today 12-m')
        trends_data = pytrends.interest_over_time()
        if not trends_data.empty:
            avg_interest = trends_data[idea].mean()
            if avg_interest > 50:
                return "High Demand"
            elif avg_interest > 20:
                return "Moderate Demand"
            else:
                return "Low Demand"
        return "Market data unavailable"

    except Exception as e:
        return f"Error fetching market demand: {str(e)}"

# API route to validate startup ideas
@app.post("/validate")
async def validate_idea(request: IdeaRequest):
    idea = request.idea

    try:
        competitors = get_competitors(idea)
        market_demand = get_market_demand(idea)

        # AI-generated insights
        ai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert startup idea validator."},
                {"role": "user", "content": f"Analyze the market demand and competitor insights for {idea}. Provide key takeaways."}
            ],
            max_tokens=100
        )
        
        validation_result = ai_response["choices"][0]["message"]["content"]
        # validation_result = "HEllo"
      
        return {
            "marketDemand": market_demand,
            "competitors": competitors,
            "pricingStrategy": "Freemium",  
            "growthPotential": "Moderate", 
            "aiAnalysis": validation_result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))