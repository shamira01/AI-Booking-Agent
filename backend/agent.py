"""
AI Booking Agent for processing chat messages and handling appointment bookings.
"""

import logging
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class BookingAgent:
    """AI agent for handling booking conversations and appointments"""

    def __init__(self, calendar_service=None):
        """Initialize BookingAgent with optional calendar service"""
        self.calendar_service = calendar_service
        self.services = {
            "haircut": {"duration": 60, "name": "Haircut"},
            "styling": {"duration": 90, "name": "Hair Styling"},
            "coloring": {"duration": 120, "name": "Hair Coloring"},
            "consultation": {"duration": 30, "name": "Consultation"}
        }

    async def process_message(
        self,
        message: str,
        session_id: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Process user message and determine intent and response
        """
        try:
            message_lower = message.lower().strip()

            # Detect booking intent
            if self._is_booking_request(message_lower):
                return await self._handle_booking_request(message, session_id)

            # Detect availability inquiry
            elif self._is_availability_request(message_lower):
                return await self._handle_availability_request(message, session_id)

            # Detect service inquiry
            elif self._is_service_inquiry(message_lower):
                return await self._handle_service_inquiry(message, session_id)

            # General greeting or conversation
            else:
                return await self._handle_general_conversation(message, session_id)

        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {
                "message": "I'm sorry, I encountered an error. Please try again.",
                "intent": "error",
                "booking_data": None,
                "suggested_times": [],
                "requires_confirmation": False
            }

    def _is_booking_request(self, message: str) -> bool:
        """Check if message contains booking intent"""
        booking_keywords = [
            "book", "schedule", "appointment", "reserve", "make an appointment",
            "i want to book", "can i book", "schedule me", "i need"
        ]
        return any(keyword in message for keyword in booking_keywords)

    def _is_availability_request(self, message: str) -> bool:
        """Check if message is asking about availability"""
        availability_keywords = [
            "available", "free", "open", "when can", "what times",
            "availability", "slots", "schedule"
        ]
        return any(keyword in message for keyword in availability_keywords)

    def _is_service_inquiry(self, message: str) -> bool:
        """Check if message is asking about services"""
        service_keywords = [
            "service", "what do you offer", "price", "cost", "how much",
            "services", "haircut", "styling", "coloring"
        ]
        return any(keyword in message for keyword in service_keywords)

    async def _handle_booking_request(self, message: str, session_id: str) -> Dict[str, Any]:
        """Handle booking request messages"""

        # Extract service type if mentioned
        service_type = self._extract_service_type(message)

        # Extract date/time if mentioned
        date_time_info = self._extract_datetime_info(message)

        if service_type and date_time_info:
            return {
                "message": f"Great! I can help you book a {service_type} appointment. Let me check availability for {date_time_info}.",
                "intent": "booking_with_details",
                "booking_data": {
                    "service_type": service_type,
                    "preferred_time": date_time_info
                },
                "suggested_times": [],
                "requires_confirmation": True
            }
        elif service_type:
            return {
                "message": f"I'd be happy to book a {service_type} appointment for you! When would you prefer to come in?",
                "intent": "booking_needs_time",
                "booking_data": {"service_type": service_type},
                "suggested_times": self._get_suggested_times(),
                "requires_confirmation": False
            }
        else:
            return {
                "message": "I'd be happy to help you book an appointment! What service are you interested in? We offer haircuts, styling, coloring, and consultations.",
                "intent": "booking_needs_service",
                "booking_data": None,
                "suggested_times": [],
                "requires_confirmation": False
            }

    async def _handle_availability_request(self, message: str, session_id: str) -> Dict[str, Any]:
        """Handle availability inquiry messages"""

        date_info = self._extract_datetime_info(message)

        if date_info:
            return {
                "message": f"Let me check our availability for {date_info}. I'll show you the open time slots.",
                "intent": "check_availability",
                "booking_data": {"requested_date": date_info},
                "suggested_times": self._get_suggested_times(),
                "requires_confirmation": False
            }
        else:
            return {
                "message": "I can check our availability for you! What date are you looking for?",
                "intent": "availability_needs_date",
                "booking_data": None,
                "suggested_times": self._get_suggested_times(),
                "requires_confirmation": False
            }

    async def _handle_service_inquiry(self, message: str, session_id: str) -> Dict[str, Any]:
        """Handle service information requests"""

        services_info = []
        for key, service in self.services.items():
            services_info.append(f"• {service['name']} ({service['duration']} minutes)")

        services_text = "\n".join(services_info)

        return {
            "message": f"Here are our available services:\n\n{services_text}\n\nWould you like to book any of these services?",
            "intent": "service_information",
            "booking_data": None,
            "suggested_times": [],
            "requires_confirmation": False
        }

    async def _handle_general_conversation(self, message: str, session_id: str) -> Dict[str, Any]:
        """Handle general conversation and greetings"""

        greetings = ["hello", "hi", "hey", "good morning", "good afternoon"]

        if any(greeting in message.lower() for greeting in greetings):
            return {
                "message": "Hello! Welcome to TailorTalk. I'm here to help you book appointments for our salon services. How can I assist you today?",
                "intent": "greeting",
                "booking_data": None,
                "suggested_times": [],
                "requires_confirmation": False
            }
        else:
            return {
                "message": "I'm here to help you with booking appointments and information about our services. Would you like to book an appointment or learn about our services?",
                "intent": "general",
                "booking_data": None,
                "suggested_times": [],
                "requires_confirmation": False
            }

    def _extract_service_type(self, message: str) -> Optional[str]:
        """Extract service type from message"""
        message_lower = message.lower()

        for service_key, service_info in self.services.items():
            if service_key in message_lower or service_info['name'].lower() in message_lower:
                return service_info['name']

        return None

    def _extract_datetime_info(self, message: str) -> Optional[str]:
        """Extract date/time information from message"""
        # Simple pattern matching for common date/time expressions
        patterns = [
            r'tomorrow',
            r'today',
            r'next week',
            r'monday|tuesday|wednesday|thursday|friday|saturday|sunday',
            r'\d{1,2}[:/]\d{1,2}',  # Time like 2:30 or 14:30
            r'\d{1,2}(am|pm)',      # Time like 2pm
        ]

        for pattern in patterns:
            if re.search(pattern, message.lower()):
                # For demo purposes, return a simplified version
                return "the requested time"

        return None

    def _get_suggested_times(self) -> List[str]:
        """Get suggested appointment times"""
        # Generate some sample time slots for the next few days
        suggested = []
        base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)

        for i in range(3):  # Next 3 days
            day = base_time + timedelta(days=i+1)
            if day.weekday() < 5:  # Monday to Friday
                suggested.extend([
                    f"{day.strftime('%A, %B %d')} at 9:00 AM",
                    f"{day.strftime('%A, %B %d')} at 2:00 PM",
                    f"{day.strftime('%A, %B %d')} at 4:00 PM"
                ])

        return suggested[:6]  # Return first 6 suggestions
