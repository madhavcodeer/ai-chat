# 🚀 AI Chat Application

A **production-quality AI Chat Application** with persistent chat history, built with a modern React frontend and FastAPI backend with SQLite database storage.

![AI Chat](https://img.shields.io/badge/React-18.3-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?logo=google)

## ✨ Features

### Frontend
- 🎨 **Modern, World-Class UI** - Glassmorphism design with smooth animations
- 💬 **Chat Interface** - Left-aligned AI messages, right-aligned user messages
- 📜 **Auto-Scroll** - Automatically scrolls to latest message
```
ai-chat-app/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # SQLite database manager
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── chat.db             # SQLite database (created on first run)
│
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── ChatMessage.jsx      # Message component
    │   │   ├── ChatMessage.css
    │   │   ├── ChatInput.jsx        # Input component
    │   │   ├── ChatInput.css
    │   │   ├── LoadingIndicator.jsx # Loading component
    │   │   └── LoadingIndicator.css
    │   ├── App.jsx                  # Main app component
    │   ├── App.css                  # App styles
    │   ├── index.css                # Global styles
    │   └── main.jsx                 # Entry point
    ├── package.json
    └── vite.config.js
```

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **Google Gemini API Key** (Get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env and add your Google Gemini API key
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

6. **Run the backend server:**
   ```bash
   python main.py
   ```

   The backend will start at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

   The frontend will start at `http://localhost:5173`

## 🎯 Usage

1. **Start both servers** (backend on port 8000, frontend on port 5173)
2. **Open your browser** to `http://localhost:5173`
3. **Start chatting!** Type a message and press Enter
4. **Chat history persists** - Refresh the page and your conversation is still there

## 🔌 API Endpoints

### `GET /`
Health check endpoint
```json
{
  "status": "online",
  "service": "AI Chat API",
  "ai_enabled": true
}
```

### `GET /messages`
Fetch all chat messages
```json
[
  {
    "message_id": 1,
    "role": "user",
    "content": "Hello!",
    "timestamp": "2025-12-10T22:30:00.000000"
  },
  {
    "message_id": 2,
    "role": "assistant",
    "content": "Hi! How can I help you?",
    "timestamp": "2025-12-10T22:30:01.000000"
  }
]
```

### `POST /messages`
Send a user message and get AI response
```json
// Request
{
  "content": "What is AI?"
}

// Response
[
  // ... all previous messages
  {
    "message_id": 3,
    "role": "user",
    "content": "What is AI?",
    "timestamp": "2025-12-10T22:30:05.000000"
  },
  {
    "message_id": 4,
    "role": "assistant",
    "content": "AI stands for Artificial Intelligence...",
    "timestamp": "2025-12-10T22:30:06.000000"
  }
]
```

### `DELETE /messages`
Clear all messages (useful for testing)
```json
{
  "status": "success",
  "message": "All messages cleared"
}
```

## 💾 Database Schema

```sql
CREATE TABLE messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,              -- 'user' or 'assistant'
    content TEXT NOT NULL,            -- Message text
    timestamp TEXT NOT NULL           -- ISO format timestamp
);
```

## 🎨 Design Features

- **Glassmorphism UI** - Modern frosted glass effects
- **Gradient Accents** - Beautiful purple-blue gradients
- **Smooth Animations** - Message slide-ins, button hover effects
- **Dark Theme** - Easy on the eyes
- **Responsive Layout** - Mobile-first design
- **Micro-interactions** - Delightful user experience

## 🛠️ Tech Stack

### Frontend
- **React 18.3** - UI library
- **Vite** - Build tool and dev server
- **CSS3** - Modern styling with custom properties

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite** - Lightweight database
- **Google Gemini API** - AI model integration
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
GEMINI_API_KEY=your_google_gemini_api_key
```

**Note:** The app will work without an API key (with simulated responses) for testing purposes.

## 📝 Development Notes

### Running in Production

**Backend:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
npm run build
npm run preview
```

### Testing Without API Key

The backend includes a fallback mechanism. If `GEMINI_API_KEY` is not set, it will return simulated responses, allowing you to test the full application flow without an API key.

## 🚨 Troubleshooting

### Backend won't start
- Ensure Python virtual environment is activated
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify port 8000 is not in use

### Frontend can't connect to backend
- Ensure backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify `API_BASE_URL` in `App.jsx` matches your backend URL

### Messages not persisting
- Check that `chat.db` file is created in the backend directory
- Verify database permissions
- Check backend logs for database errors

## 🎯 Future Enhancements

- [ ] User authentication
- [ ] Multiple conversation threads
- [ ] Message editing and deletion
- [ ] Code syntax highlighting
- [ ] File attachments
- [ ] Voice input
- [ ] Export conversation history
- [ ] Dark/Light theme toggle

## 📄 License

MIT License - Feel free to use this project for learning or production!

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

**Built with ❤️ using React, FastAPI, and Google Gemini AI**
