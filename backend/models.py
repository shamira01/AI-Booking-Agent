"""
Pydantic models for request and response validation.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., description="User's message")
    session_id: str = Field(default="default", description="Session identifier")
    conversation_history: List[Dict[str, str]] = Field(
        default=[], 
        description="Previous conversation exchanges"
    )

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    message: str = Field(..., description="Agent's response message")
    booking_data: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Extracted booking information"
    )
    suggested_times: List[str] = Field(
        default=[], 
        description="Suggested available time slots"
    )
    requires_confirmation: bool = Field(
        default=False, 
        description="Whether the booking requires user confirmation"
    )

class BookingRequest(BaseModel):
    """Request model for booking endpoint"""
    title: str = Field(..., description="Appointment title")
    description: str = Field(default="", description="Appointment description")
    start_time: datetime = Field(..., description="Start time of the appointment")
    end_time: datetime = Field(..., description="End time of the appointment")
    attendee_email: Optional[str] = Field(
        default=None, 
        description="Email of the attendee"
    )

class BookingResponse(BaseModel):
    """Response model for booking endpoint"""
    success: bool = Field(..., description="Whether the booking was successful")
    message: str = Field(..., description="Status message")
    event_id: Optional[str] = Field(
        default=None, 
        description="Google Calendar event ID"
    )
    event_details: Optional[Dict[str, Any]] = Field(
        default=None, 
        description="Full event details from Google Calendar"
    )

class AvailabilitySlot(BaseModel):
    """Model for available time slots"""
    start: datetime = Field(..., description="Start time of the slot")
    end: datetime = Field(..., description="End time of the slot")

class ConversationEntry(BaseModel):
    """Model for conversation history entries"""
    user: str = Field(..., description="User's message")
    assistant: str = Field(..., description="Assistant's response")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp")