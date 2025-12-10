# Quick Start Guide

## 🚀 Quick Start (5 minutes)

### Step 1: Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (optional - works without it)
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY if you have one

# Start backend
python main.py
```

Backend should now be running at http://localhost:8000

### Step 2: Frontend Setup (New Terminal)
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend should now be running at http://localhost:5173

### Step 3: Start Chatting! 🎉
Open http://localhost:5173 in your browser and start chatting!

## 🔑 Getting a Google Gemini API Key (Optional)

1. Go to https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in `backend/.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```

**Note:** The app works without an API key (with simulated responses) for testing!

## 🎯 Test the API

Visit http://localhost:8000 to see the health check:
```json
{
  "status": "online",
  "service": "AI Chat API",
  "ai_enabled": true
}
```

## 📱 Features to Try

1. **Send a message** - Type and press Enter
2. **Refresh the page** - Your chat history persists!
3. **Try keyboard shortcuts** - Enter to send, Shift+Enter for new line
4. **Watch the animations** - Smooth message slide-ins and loading states

## 🛑 Stopping the Servers

- Press `Ctrl+C` in each terminal window to stop the servers

## 💡 Tips

- Keep both terminal windows open while using the app
- Check the browser console (F12) for any errors
- Backend logs will show in the backend terminal
- The database file `chat.db` is created automatically in the backend folder
