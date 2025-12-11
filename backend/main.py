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
from fastapi.staticfiles import StaticFiles

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="AI Chat API", version="1.0.0")

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    # Using gemini-2.0-flash-exp (verified availability)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    print(f"✅ AI Model configured: gemini-2.0-flash-exp")
else:
    model = None
    print("⚠️  Warning: GEMINI_API_KEY not set. AI responses will be simulated.")


# Pydantic models for request/response validation
class MessageRequest(BaseModel):
    content: str
    api_key: Optional[str] = None


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
        try:
            ai_response = await generate_ai_response(message.content, message.api_key)
        except Exception as ai_error:
            print(f"❌ AI Generation Critical Fail: {ai_error}")
            ai_response = "I apologize, but I am unable to generate a response at this time. Please try again later."
        
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
    
    except Exception as e:
        import traceback
        print(f"❌ Critical Endpoint Error:\n{traceback.format_exc()}")
        # Fallback: try to return whatever messages we have, plus an error message
        try:
            error_msg = f"System Error: {str(e)}"
            db.add_message("assistant", error_msg, datetime.now().isoformat())
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
        except:
             # Just raise if even the fallback fails
             raise HTTPException(status_code=500, detail=f"Critical system failure: {str(e)}")


async def generate_ai_response(user_message: str, user_api_key: Optional[str] = None) -> str:
    """
    Generate AI response using Google Gemini API
    Uses user_api_key if provided, otherwise falls back to server env key
    """
    try:
        current_model = None
        
        # 1. Try User API Key first
        if user_api_key and user_api_key.strip():
            try:
                # Configure a temporary client for this request
                genai.configure(api_key=user_api_key)
                current_model = genai.GenerativeModel('gemini-2.0-flash-exp')
                print("🔑 Using User provided API Key")
            except Exception as e:
                print(f"User Key Config Error: {e}")
                pass 

        # 2. Fallback to System API Key if no user key provided
        if not current_model and model:
            # We must re-configure if we switched keys, to be safe, 
            # but usually 'model' object retains its config. 
            # Simpler approach: If system key exists, use global model.
            current_model = model
            print("🔒 Using System API Key")

        if current_model:
            response = current_model.generate_content(user_message)
            return response.text
        else:
            return "Please provide a Gemini API Key in Settings to chat!"
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ AI Generation Error:\n{error_details}")
        return f"I apologize, but I encountered an error. Error: {str(e)}"


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


# Mount the frontend/dist directory to serve the React app
# This must be after all API routes
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "dist")

if os.path.exists(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
else:
    print(f"⚠️ Frontend dist folder not found at {frontend_dist}. Run 'npm run build' in frontend directory first.")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
