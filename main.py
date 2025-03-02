from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import TravelQuery, Base
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
import uvicorn

# Load environment variables
load_dotenv()

# Initialize database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(title="AI Travel Planner", version="1.0", description="Generate AI-powered travel itineraries")

# LLM Configuration
llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="deepseek-r1-distill-qwen-32b", temperature=0.7)

# Prompt Template
template = """  
You are an AI travel planner. Create a **day-by-day travel itinerary** based on user preferences.

### **User Details:**  
- Destination: {destination}  
- Travel Dates: {dates}  
- Budget: {budget}  
- Preferences: {preferences}  
- Number of Travelers: {num_travelers}  
- Accommodation Type: {accommodation}  

### **Itinerary:**  
Day 1  
🌅 Morning: [Activity] at [Location] – [Brief Description]  
🌞 Afternoon: [Activity] at [Location] – [Brief Description]  
🌙 Evening: [Activity] at [Location] – [Brief Description]  

Day 2  
...  
"""

prompt = PromptTemplate(
    input_variables=["destination", "dates", "budget", "preferences", "num_travelers", "accommodation"],
    template=template
)

chain = LLMChain(llm=llm, prompt=prompt)

# Dependency: Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request Model
class TravelRequest(BaseModel):
    destination: str
    dates: str
    budget: str
    preferences: str
    num_travelers: int
    accommodation: str

@app.get("/")
def home():
    return {"message": "Welcome to AI Travel Planner"}

@app.post("/generate_itinerary/")
def generate_itinerary(request: TravelRequest, db: Session = Depends(get_db)):
    try:
        response = chain.run({
            "destination": request.destination,
            "dates": request.dates,
            "budget": request.budget,
            "preferences": request.preferences,
            "num_travelers": request.num_travelers,
            "accommodation": request.accommodation
        })

        # Store in database
        itinerary_entry = TravelQuery(
            destination=request.destination,
            dates=request.dates,
            budget=request.budget,
            preferences=request.preferences,
            num_travelers=request.num_travelers,
            accommodation=request.accommodation,
            response=response
        )

        db.add(itinerary_entry)
        db.commit()
        db.refresh(itinerary_entry)

        return {"itinerary": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
