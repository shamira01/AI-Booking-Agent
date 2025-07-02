TailorTalk AI Booking Agent

TailorTalk is an AI-powered conversational booking system for salons. It helps clients schedule appointments through natural conversation, checks real-time availability, and integrates with Google Calendar — all with a friendly chat interface!

✨ Features

✅ Natural Conversation Flow — Chat with an AI agent to book services like haircuts, styling, and coloring.
✅ Smart Availability Checking — Finds free time slots based on your preferences and working hours.
✅ Google Calendar Integration — Syncs appointments seamlessly with your calendar.
✅ Rich Chat UI — Clean and interactive Streamlit frontend for conversations and confirmations.
✅ Async FastAPI Backend — Handles chat logic, booking workflows, and calendar API calls.

🏗️ Architecture Overview
Frontend: Streamlit

frontend/
└── streamlit_app.py — Main Streamlit app
Chat-like interface for users to talk to the AI.

Displays booking details, available slots, and confirmation messages.

Backend: FastAPI

backend/
├── app.py — FastAPI server with routes
├── agent.py — BookingAgent class: processes chat, intents, and booking logic
├── calendar_service.py — Connects to Google Calendar API
├── models.py — Request/Response models (Pydantic)
/chat — Processes chat messages and detects intents.

/availability — Checks calendar for open time slots.

/book — Creates new appointments.

/events — Retrieves calendar events.

Static

static/ — Optional folder for static assets
💼 Example Conversation Flows
🗨️ “Hi! I’d like to book a haircut next Tuesday at 2pm.”
— Detects intent ➝ Extracts service ➝ Checks availability ➝ Confirms booking ➝ Adds to Google Calendar

🗨️ “What services do you offer?”
— Lists haircut, styling, coloring, and consultation with durations.

🗨️ “When is your next available slot for hair coloring?”
— Finds open slots within working hours (9 AM–5 PM) excluding weekends.


Output Screenshots
![image](https://github.com/user-attachments/assets/e61d062f-ae54-4bee-a574-ad57599777d8)
![image](https://github.com/user-attachments/assets/1e808eea-d369-4623-982b-edd45423c244)
![image](https://github.com/user-attachments/assets/beb8453b-94dc-4c5b-8a80-ab6ee4e1fc84)
![image](https://github.com/user-attachments/assets/caba3850-dd32-4afd-8d9b-492a63faa364)


🚀 Getting Started

1. Clone the repo
git clone https://github.com/shamira01/AI-Booking-Agent.git
cd AI-Booking-Agent

2. Create and activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run the FastAPI backend
cd backend
uvicorn app:app --reload --port 8000

5. Run the Streamlit frontend
cd ../frontend
streamlit run streamlit_app.py

Backend ➝ http://localhost:8000
Frontend ➝ http://localhost:8501
