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

🗝️ Environment Variables

export GOOGLE_CALENDAR_CREDENTIALS= {
  "type": "service_account",
  "project_id": "npschatbot-439607",
  "private_key_id": "a1dd23740921c1789eb29c19d830d44b8f6bca28",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCbiO2NhUZOFTx5\nlXolXI/nrPrNgfDuUF6rWKJ8U4FqH6P+RXQ65iO49jRB1vAUYqloBupZlvw/J7BE\nRbsCjt78BqOs/R8E1bZ2LDyOtZQKsGUYCW2K3W9WZfhy9/9GH2gMU0hwUlUCJU3F\nzs8AQ+EGK31X8EZq3yuNLqTRMA42gk1AFcb2Mr2iY2vD+uQJb7nbNI7bt8kKY5al\nXp6OKf8Ng2AI240zKjwl13ZG8sXNuhjeEzZllkXRvzBvJI3ixQdlPVP4gL/psK42\nFmbeXbgVjfFraAUCO7xxPCZYbSFNZHS9ldaLNNQbLX4wtBL3kKtJTvMnBTCR3v9W\nDills87BAgMBAAECggEACHw65+3UCeFMtrfGvZBEMl5674h3ekW2NHp8bg310Uu/\naNk/LKtuwK6ytFjWj8+/vQyLiOG2cN4CCgEUri0/N9hHSHu/gnlqUx4f6HIHJpVW\nOC59F6AnBjtzIRde8BafvyeYAlC4XiQzQjRn99q8K9fMwDLVx9gIpAYq0oktoIZh\n78eyd2GhTjE1j+4ObSpoSbqjqbtwuJvDjhddWjJbF5P2JRjtvxxRwht2N2DA0My+\n5KnGdZ6nnKaVpz2XS9ggMtbRUAjLHqmaMZz2a1B/GSb/B35FTIMyqk0NxJIQy3be\nXmTxKLBjripOFH5f7TXw2JbVSXH3VkdZcAXZ5hu6BQKBgQDOndh6srczeOxgum5N\nI13o5IfmQt92533auP0w4mA0BxhzAy0NHzp5v9moEXSEP++HcFTQSX7E6tAYHzF5\n4c29Hz+ZB0O75sIWabMwkvcILsgNAQr9QXxuQms3K6jyUKwmNimSr9CEb6zGFRGL\nSH5dif/Np2aDEcesu5t2NDo5ZwKBgQDAtZGyddqMFEquyq7GS+0GLnh9uYtuuuJ1\nF6IJlz7ac9kNgp55FjzEjw9aYqWFrYb/0k8JhDgfVPSSdfOrdvY6NXNF25CBR4uJ\ndn+06+RqnhAvpZHbjEzcZx06CdoCg5ig3WveEVMvxJ8LvL8C3cAH4nk990ZLped8\nO9fgfZWVlwKBgEUxEPzN+pHvLeGarTOB44IJfgU7YdBU542mo4uKU8M4mRRy/NRH\nH/MDr2UcK1PagWFu2chCxIQ3Sma5k30IhDiQTWD20NUNCvQsg4iBvt5rpCzOq5py\nIrRd47+/DD3RjETjoHpyDDc9mrNe/NgS99ZlT1fUdnzwKFkNHpuwE8uDAoGAJk+y\nkH0XnsOl+Uv4JRoRHCp+79fEXZYv0UGKiEeWSk2/uAzgvofqOtWKItj7uTC/ZvqD\nlgvAMJJuMPPcJpl26CmaKig1eU4k8oYpa2l+NqgH5cEP10r0ONkTGWe9/MP2wvxi\nJnrhQ9zeFbJHcyVsuOSQX/5Z7k4kUDGBgHLXGy8CgYEAyc0ozdZbfYzH0fhV4LEg\nTELCnFEo4BpD/zPh3VA7VPhsGqTx0X6915MexyYcggStES8iWETN/uIDqPL20/Zw\nCp7IKLERWdVjg1w8ZPgbPSiXrpweU6E2Y/yZMFsKoHRCBL1gJyYGSIiNJs82H8eA\ndqgPkq1I/VymvwyP7CeViYg=\n-----END PRIVATE KEY-----\n",
  "client_email": "calendar-service-account@npschatbot-439607.iam.gserviceaccount.com",
  "client_id": "109619400152536242229",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/calendar-service-account%40npschatbot-439607.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

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
