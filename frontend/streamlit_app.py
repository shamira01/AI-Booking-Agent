"""
Streamlit frontend for TailorTalk AI booking agent.
"""

import streamlit as st
import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Configure Streamlit page
st.set_page_config(
    page_title="TailorTalk AI Booking Assistant",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend API base URL
API_BASE_URL = "http://localhost:8000"

def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm TailorTalk, your AI booking assistant. I can help you schedule appointments in your calendar. What would you like to book today?"
            }
        ]
    if "session_id" not in st.session_state:
        st.session_state.session_id = "default"
    if "booking_in_progress" not in st.session_state:
        st.session_state.booking_in_progress = None

def send_chat_message(message: str) -> Dict[str, Any]:
    """Send a chat message to the backend"""
    try:
        # Prepare conversation history
        conversation_history = []
        for i in range(0, len(st.session_state.messages) - 1, 2):
            if i + 1 < len(st.session_state.messages):
                conversation_history.append({
                    "user": st.session_state.messages[i].get("content", ""),
                    "assistant": st.session_state.messages[i + 1].get("content", "")
                })
        
        payload = {
            "message": message,
            "session_id": st.session_state.session_id,
            "conversation_history": conversation_history[-5:]  # Last 5 exchanges
        }
        
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return {
                "message": "I'm sorry, I'm having trouble connecting to my systems. Please try again.",
                "booking_data": None,
                "suggested_times": [],
                "requires_confirmation": False
            }
    
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return {
            "message": "I'm having trouble connecting to my systems. Please check your connection and try again.",
            "booking_data": None,
            "suggested_times": [],
            "requires_confirmation": False
        }

def book_appointment(booking_data: Dict[str, Any]) -> Dict[str, Any]:
    """Book an appointment using the backend API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/book",
            json=booking_data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "success": False,
                "message": f"Booking failed: {response.text}"
            }
    
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Connection error: {e}"
        }

def display_suggested_times(suggested_times: List[str]):
    """Display suggested time slots as clickable buttons"""
    if suggested_times:
        st.write("**Available time slots:**")
        cols = st.columns(min(len(suggested_times), 3))
        
        for i, time_slot in enumerate(suggested_times):
            with cols[i % 3]:
                if st.button(f"📅 {time_slot}", key=f"time_slot_{i}"):
                    # User selected a time slot
                    confirmation_message = f"I'd like to book the appointment for {time_slot}"
                    st.session_state.messages.append({
                        "role": "user",
                        "content": confirmation_message
                    })
                    
                    # Send confirmation message
                    response = send_chat_message(confirmation_message)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["message"]
                    })
                    
                    st.rerun()

def display_chat_message(message: Dict[str, str]):
    """Display a chat message with proper styling"""
    with st.chat_message(message["role"]):
        st.write(message["content"])

def main():
    """Main Streamlit app"""
    init_session_state()
    
    # App header
    st.title("📅 TailorTalk AI Booking Assistant")
    st.markdown("---")
    
    # Sidebar with app info
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        TailorTalk is your intelligent booking assistant that can:
        
        ✅ **Check calendar availability**  
        ✅ **Suggest optimal time slots**  
        ✅ **Book appointments naturally**  
        ✅ **Handle scheduling conflicts**  
        ✅ **Confirm booking details**
        
        Just tell me what you'd like to schedule!
        """)
        
        st.header("🔧 Quick Actions")
        if st.button("🗑️ Clear Conversation"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Hello! I'm TailorTalk, your AI booking assistant. How can I help you schedule an appointment today?"
                }
            ]
            st.session_state.booking_in_progress = None
            st.rerun()
        
        # Calendar view section
        st.header("📊 Calendar Overview")
        
        # Date range selector for viewing availability
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From", datetime.now().date())
        with col2:
            end_date = st.date_input("To", (datetime.now() + timedelta(days=7)).date())
        
        if st.button("Check Availability"):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/availability",
                    params={
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat(),
                        "duration_minutes": 60
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    available_slots = data.get("available_slots", [])
                    
                    if available_slots:
                        st.success(f"Found {len(available_slots)} available slots!")
                        for slot in available_slots[:5]:  # Show first 5
                            start_time = datetime.fromisoformat(slot["start"])
                            st.write(f"• {start_time.strftime('%b %d, %Y at %I:%M %p')}")
                    else:
                        st.warning("No available slots found in this date range.")
                else:
                    st.error("Failed to check availability.")
            except Exception as e:
                st.error(f"Error checking availability: {e}")
    
    # Main chat interface
    st.header("💬 Chat with TailorTalk")
    
    # Display chat messages
    for message in st.session_state.messages:
        display_chat_message(message)
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message immediately
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("TailorTalk is thinking..."):
                response = send_chat_message(prompt)
            
            # Display assistant message
            st.write(response["message"])
            
            # Display suggested times if available
            if response.get("suggested_times"):
                display_suggested_times(response["suggested_times"])
            
            # Handle booking confirmation
            if response.get("requires_confirmation") and response.get("booking_data"):
                st.session_state.booking_in_progress = response["booking_data"]
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Confirm Booking", type="primary"):
                        booking_result = book_appointment(st.session_state.booking_in_progress)
                        if booking_result.get("success"):
                            st.success(booking_result["message"])
                            st.session_state.booking_in_progress = None
                        else:
                            st.error(booking_result["message"])
                        st.rerun()
                
                with col2:
                    if st.button("❌ Cancel"):
                        st.session_state.booking_in_progress = None
                        st.info("Booking cancelled.")
                        st.rerun()
        
        # Add assistant response to messages
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["message"]
        })
    
    # Sample conversation starters
    st.markdown("---")
    st.subheader("💡 Try these examples:")
    
    examples = [
        "I need to schedule a doctor's appointment next week",
        "Can you book a 1-hour meeting with the team tomorrow afternoon?",
        "What time slots are available on Friday?",
        "Schedule a call with client for next Monday at 2 PM",
        "I want to book a 30-minute consultation this week"
    ]
    
    cols = st.columns(2)
    for i, example in enumerate(examples):
        with cols[i % 2]:
            if st.button(f"💬 {example}", key=f"example_{i}"):
                # Add example to chat
                st.session_state.messages.append({
                    "role": "user",
                    "content": example
                })
                st.rerun()

if __name__ == "__main__":
    main()