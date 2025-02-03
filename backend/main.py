import openai 
from fastapi import FastAPI 
from pydantic import BaseModel 
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Allow CORS from specific origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class IdeaRequest(BaseModel):
    idea: str

@app.post("/validate")
async def validate_idea(request: IdeaRequest):
    idea = request.idea

    # Use OpenAI to analyze the idea
    response = openai.Completion.create(
        model="gpt-3.5-turbo", 
        prompt=f"Validate this startup idea: {idea}",
        max_tokens=200
    )
    
    validation_result = response.choices[0].text.strip()
    
    # Return a simulated validation result for now
    return {
        "marketDemand": "High",
        "competitors": ["Competitor A", "Competitor B"],
        "pricingStrategy": "Freemium",
        "growthPotential": "Moderate",
        "aiAnalysis": validation_result
    }
