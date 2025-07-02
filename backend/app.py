"""
FastAPI backend for TailorTalk AI booking agent.
Handles chat interactions and calendar operations.
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from models import ChatRequest, ChatResponse, BookingRequest, BookingResponse
from agent import BookingAgent
from calendar_service import GoogleCalendarService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TailorTalk AI Booking Agent", version="1.0.0")

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
calendar_service = GoogleCalendarService()
booking_agent = BookingAgent(calendar_service)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        # Test calendar service connection
        await calendar_service.test_connection()
        logger.info("Calendar service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize calendar service: {e}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "TailorTalk AI Booking Agent is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle chat interactions with the booking agent.
    """
    try:
        logger.info(f"Received chat request: {request.message}")
        
        # Process message through the booking agent
        response = await booking_agent.process_message(
            message=request.message,
            session_id=request.session_id,
            conversation_history=request.conversation_history
        )
        
        logger.info(f"Agent response: {response}")
        
        return ChatResponse(
            message=response.get("message", "I'm sorry, I couldn't process that request."),
            booking_data=response.get("booking_data"),
            suggested_times=response.get("suggested_times", []),
            requires_confirmation=response.get("requires_confirmation", False)
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/book", response_model=BookingResponse)
async def book_appointment(request: BookingRequest):
    """
    Book an appointment in the calendar.
    """
    try:
        logger.info(f"Booking appointment: {request}")
        
        # Create the event in Google Calendar
        event = await calendar_service.create_event(
            title=request.title,
            description=request.description,
            start_time=request.start_time,
            end_time=request.end_time,
            attendee_email=request.attendee_email
        )
        
        return BookingResponse(
            success=True,
            event_id=event.get("id"),
            message=f"Appointment booked successfully for {request.start_time.strftime('%B %d, %Y at %I:%M %p')}",
            event_details=event
        )
        
    except Exception as e:
        logger.error(f"Error booking appointment: {e}")
        return BookingResponse(
            success=False,
            message=f"Failed to book appointment: {str(e)}"
        )

@app.get("/availability")
async def check_availability(
    start_date: str, 
    end_date: str, 
    duration_minutes: int = 60
):
    """
    Check calendar availability for a given date range.
    """
    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        
        available_slots = await calendar_service.get_available_slots(
            start_time=start_dt,
            end_time=end_dt,
            duration_minutes=duration_minutes
        )
        
        return {
            "available_slots": [
                {
                    "start": slot["start"].isoformat(),
                    "end": slot["end"].isoformat()
                }
                for slot in available_slots
            ]
        }
        
    except Exception as e:
        logger.error(f"Error checking availability: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/events")
async def get_events(start_date: str, end_date: str):
    """
    Get events from the calendar for a given date range.
    """
    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        
        events = await calendar_service.get_events(start_dt, end_dt)
        
        return {"events": events}
        
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
