from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

class TravelQuery(Base):
    __tablename__ = "travel_queries"

    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, index=True)
    dates = Column(String)
    budget = Column(String)
    preferences = Column(Text)
    num_travelers = Column(Integer)
    accommodation = Column(String)
    response = Column(Text)
    created_at = Column(DateTime, default=func.now())
