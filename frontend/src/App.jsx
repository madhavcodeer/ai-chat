import { useState, useEffect, useRef } from 'react'
import './App.css'
import ChatMessage from './components/ChatMessage'
import ChatInput from './components/ChatInput'
import LoadingIndicator from './components/LoadingIndicator'

const API_BASE_URL = '/api'

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  // Auto-scroll to latest message
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Fetch chat history on component mount
  useEffect(() => {
    fetchChatHistory()
  }, [])

  const fetchChatHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/messages`)
      if (!response.ok) {
        throw new Error('Failed to fetch chat history')
      }
      const data = await response.json()
      setMessages(data)
    } catch (err) {
      console.error('Error fetching chat history:', err)
      setError('Failed to load chat history. Make sure the backend is running.')
    }
  }

  const sendMessage = async (content) => {
    if (!content.trim()) return

    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE_URL}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content }),
      })

      if (!response.ok) {
        throw new Error('Failed to send message')
      }

      const updatedMessages = await response.json()
      setMessages(updatedMessages)
    } catch (err) {
      console.error('Error sending message:', err)
      setError('Failed to send message. Please check your connection and try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">✨</div>
            <h1>AI Chat</h1>
          </div>
          <div className="status-indicator">
            <span className="status-dot"></span>
            <span className="status-text">Online</span>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <main className="chat-container">
        <div className="messages-wrapper">
          {messages.length === 0 && !error && (
            <div className="empty-state">
              <div className="empty-icon">💬</div>
              <h2>Start a conversation</h2>
              <p>Send a message to begin chatting with AI</p>
            </div>
          )}

          {error && (
            <div className="error-banner">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}

          {messages.map((message) => (
            <ChatMessage
              key={message.message_id}
              role={message.role}
              content={message.content}
              timestamp={message.timestamp}
            />
          ))}

          {isLoading && <LoadingIndicator />}

          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Area */}
      <ChatInput onSendMessage={sendMessage} disabled={isLoading} />
    </div>
  )
}

export default App
