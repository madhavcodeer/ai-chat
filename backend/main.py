"""
FastAPI Backend for AI Chat Application
Handles chat message storage and AI integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv
from database import Database

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="AI Chat API", version="1.0.0")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = Database()

# Configure Google Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Using bleeding edge gemini-2.5-flash found in your model list
    model = genai.GenerativeModel('gemini-2.5-flash')
    print(f"✅ AI Model configured: gemini-2.5-flash")
else:
    model = None
    print("⚠️  Warning: GEMINI_API_KEY not set. AI responses will be simulated.")


# Pydantic models for request/response validation
class MessageRequest(BaseModel):
    content: str


class MessageResponse(BaseModel):
    message_id: int
    role: str
    content: str
    timestamp: str


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    db.create_tables()
    print("✅ Database initialized successfully")


@app.get("/api")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "AI Chat API",
        "ai_enabled": model is not None
    }


@app.get("/api/messages", response_model=List[MessageResponse])
async def get_messages():
    """
    Fetch all chat messages from database
    Returns messages in chronological order
    """
    try:
        messages = db.get_all_messages()
        return [
            MessageResponse(
                message_id=msg[0],
                role=msg[1],
                content=msg[2],
                timestamp=msg[3]
            )
            for msg in messages
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/api/messages", response_model=List[MessageResponse])
async def create_message(message: MessageRequest):
    """
    Process user message and generate AI response
    Stores both user message and AI reply in database
    Returns updated conversation
    """
    try:
        # Validate input
        if not message.content.strip():
            raise HTTPException(status_code=400, detail="Message content cannot be empty")
        
        # Store user message
        user_timestamp = datetime.now().isoformat()
        db.add_message("user", message.content, user_timestamp)
        
        # Generate AI response
        ai_response = await generate_ai_response(message.content)
        
        # Store AI response
        ai_timestamp = datetime.now().isoformat()
        db.add_message("assistant", ai_response, ai_timestamp)
        
        # Return updated conversation
        messages = db.get_all_messages()
        return [
            MessageResponse(
                message_id=msg[0],
                role=msg[1],
                content=msg[2],
                timestamp=msg[3]
            )
            for msg in messages
        ]
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


async def generate_ai_response(user_message: str) -> str:
    """
    Generate AI response using Google Gemini API
    Falls back to simulated response if API is not configured
    """
    try:
        if model:
            # Use Google Gemini API
            response = model.generate_content(user_message)
            return response.text
        else:
            # Simulated response for testing without API key
            return f"I received your message: '{user_message}'. (This is a simulated response. Please set GEMINI_API_KEY environment variable to enable real AI responses.)"
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ AI Generation Error:\n{error_details}")
        return f"I apologize, but I encountered an error. Error details: {str(e)}"


@app.delete("/api/messages")
async def clear_messages():
    """
    Clear all messages from database
    Useful for testing and resetting conversation
    """
    try:
        db.clear_all_messages()
        return {"status": "success", "message": "All messages cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing messages: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
