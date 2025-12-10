# 🏗️ AI Chat Application - Technical Architecture

## Overview
Production-quality AI chat application with persistent storage, modern React frontend, and FastAPI backend.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                    (React + Vite)                            │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ ChatMessage  │  │  ChatInput   │  │   Loading    │      │
│  │  Component   │  │  Component   │  │  Indicator   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              App.jsx (State Management)              │   │
│  │  - Fetch chat history on mount                       │   │
│  │  - Send messages to backend                          │   │
│  │  - Auto-scroll to latest message                     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST
                            │ (JSON)
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                         Backend                              │
│                       (FastAPI)                              │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   API Endpoints                       │   │
│  │  GET  /          - Health check                       │   │
│  │  GET  /messages  - Fetch all messages                 │   │
│  │  POST /messages  - Send message, get AI response      │   │
│  │  DELETE /messages - Clear all messages                │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│                            ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Database Manager                         │   │
│  │  - Create tables                                      │   │
│  │  - Add messages                                       │   │
│  │  - Retrieve messages                                  │   │
│  │  - Clear messages                                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                 │
│                            ▼                                 │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              SQLite Database                          │   │
│  │  Table: messages                                      │   │
│  │  - message_id (PK)                                    │   │
│  │  - role (user/assistant)                              │   │
│  │  - content (text)                                     │   │
│  │  - timestamp (ISO)                                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ API Call
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Google Gemini API                          │
│                  (AI Response Generation)                    │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Initial Page Load
```
User opens browser
    ↓
Frontend mounts
    ↓
useEffect triggers fetchChatHistory()
    ↓
GET /messages request to backend
    ↓
Backend queries SQLite database
    ↓
Returns all messages as JSON
    ↓
Frontend displays messages
    ↓
Auto-scrolls to bottom
```

### 2. Sending a Message
```
User types message and presses Enter
    ↓
ChatInput component calls onSendMessage()
    ↓
App.jsx sets isLoading = true
    ↓
POST /messages with user message
    ↓
Backend receives request
    ↓
Stores user message in database
    ↓
Calls Google Gemini API
    ↓
Receives AI response
    ↓
Stores AI response in database
    ↓
Returns updated conversation
    ↓
Frontend updates messages state
    ↓
New messages animate in
    ↓
Auto-scrolls to bottom
    ↓
Sets isLoading = false
```

## Component Hierarchy

```
App.jsx
├── Header
│   ├── Logo (icon + title)
│   └── Status Indicator
├── Chat Container
│   ├── Empty State (if no messages)
│   ├── Error Banner (if error)
│   ├── ChatMessage[] (mapped from messages array)
│   │   ├── Avatar
│   │   ├── Message Header (role + timestamp)
│   │   └── Message Content
│   ├── LoadingIndicator (if isLoading)
│   └── Auto-scroll ref
└── ChatInput
    ├── Textarea
    ├── Send Button
    └── Keyboard Hint
```

## State Management

### App.jsx State
```javascript
const [messages, setMessages] = useState([])
// Array of message objects from backend

const [isLoading, setIsLoading] = useState(false)
// True when waiting for AI response

const [error, setError] = useState(null)
// Error message string or null

const messagesEndRef = useRef(null)
// Reference for auto-scrolling
```

## API Contract

### Message Object
```typescript
interface Message {
  message_id: number;      // Auto-incremented ID
  role: "user" | "assistant";  // Message sender
  content: string;         // Message text
  timestamp: string;       // ISO format: "2025-12-10T22:30:00.000000"
}
```

### Request/Response Examples

**GET /messages**
```
Request: None
Response: Message[]
```

**POST /messages**
```
Request: { content: string }
Response: Message[]  // Full updated conversation
```

## Database Schema

```sql
CREATE TABLE messages (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    timestamp TEXT NOT NULL
);

-- Indexes for performance
CREATE INDEX idx_timestamp ON messages(timestamp);
CREATE INDEX idx_role ON messages(role);
```

## Styling Architecture

### CSS Custom Properties (Design Tokens)
```css
:root {
  /* Colors */
  --bg-primary: #0a0a0f;
  --accent-primary: #6366f1;
  
  /* Spacing */
  --spacing-md: 1rem;
  
  /* Border Radius */
  --radius-lg: 1rem;
  
  /* Shadows */
  --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.3);
}
```

### Component-Specific Styles
- Each component has its own CSS file
- Uses design tokens for consistency
- Animations defined per component
- Responsive breakpoints at 768px

## Key Features Implementation

### 1. Auto-Scroll
```javascript
useEffect(() => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
}, [messages])
```

### 2. Keyboard Shortcuts
```javascript
const handleKeyPress = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    handleSubmit(e)
  }
}
```

### 3. Loading State
```javascript
{isLoading && <LoadingIndicator />}
```

### 4. Error Handling
```javascript
try {
  // API call
} catch (err) {
  setError('Failed to send message')
}
```

## Performance Optimizations

1. **Lazy Loading**: Components loaded on demand
2. **Memoization**: Could add React.memo for message components
3. **Database Indexing**: Timestamps and roles indexed
4. **Async Operations**: All I/O is non-blocking
5. **Connection Pooling**: SQLite connection reused

## Security Considerations

1. **CORS**: Configured for localhost only
2. **Input Validation**: Pydantic models validate all inputs
3. **SQL Injection**: Using parameterized queries
4. **API Key**: Stored in environment variables
5. **Error Messages**: Generic errors sent to frontend

## Scalability Path

### Current (MVP)
- SQLite database
- Single server
- No authentication

### Future Enhancements
1. **Database**: Migrate to PostgreSQL
2. **Authentication**: Add JWT tokens
3. **Caching**: Redis for message caching
4. **Load Balancing**: Multiple backend instances
5. **CDN**: Static asset delivery
6. **WebSockets**: Real-time updates
7. **Message Queues**: Async AI processing

## Testing Strategy

### Frontend
- Component tests (React Testing Library)
- Integration tests (API mocking)
- E2E tests (Playwright/Cypress)

### Backend
- Unit tests (pytest)
- API tests (FastAPI TestClient)
- Database tests (in-memory SQLite)

## Deployment

### Frontend
```bash
npm run build
# Deploy dist/ folder to:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
```

### Backend
```bash
# Docker
docker build -t ai-chat-backend .
docker run -p 8000:8000 ai-chat-backend

# Or deploy to:
# - Render.com
# - Railway.app
# - AWS EC2/ECS
# - Google Cloud Run
```

## Environment Variables

### Backend (.env)
```
GEMINI_API_KEY=your_key_here
DATABASE_URL=sqlite:///./chat.db  # Optional
CORS_ORIGINS=http://localhost:5173,https://yourdomain.com
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## Monitoring & Logging

### Backend Logging
- FastAPI automatic request logging
- Custom error logging
- Database operation logging

### Frontend Logging
- Console errors
- API call logging
- User interaction tracking (future)

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Accessibility

- Semantic HTML
- ARIA labels (to be added)
- Keyboard navigation
- Screen reader support (to be improved)

---

**Last Updated**: December 10, 2025
**Version**: 1.0.0
