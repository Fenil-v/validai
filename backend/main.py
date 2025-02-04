import openai 
from fastapi import FastAPI 
from pydantic import BaseModel 
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
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

    try:
        # Use OpenAI Chat API instead of Completion API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "system", "content": "You are an expert startup idea validator."},
                {"role": "user", "content": f"Validate this startup idea: {idea}"}
            ],
            max_tokens=200
        )
        
        validation_result = response["choices"][0]["message"]["content"]
      
        return {
            "marketDemand": "High",
            "competitors": ["Competitor A", "Competitor B"],
            "pricingStrategy": "Freemium",
            "growthPotential": "Moderate",
            "aiAnalysis": validation_result
        }

    except Exception as e:
        return {"error": str(e)}