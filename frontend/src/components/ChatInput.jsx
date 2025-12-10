import { useState } from 'react'
import './ChatInput.css'

function ChatInput({ onSendMessage, disabled }) {
    const [input, setInput] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault()
        if (input.trim() && !disabled) {
            onSendMessage(input)
            setInput('')
        }
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSubmit(e)
        }
    }

    return (
        <div className="chat-input-container">
            <form onSubmit={handleSubmit} className="chat-input-form">
                <div className="input-wrapper">
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Type your message..."
                        disabled={disabled}
                        rows="1"
                        className="message-input"
                    />
                    <button
                        type="submit"
                        disabled={disabled || !input.trim()}
                        className="send-button"
                    >
                        {disabled ? (
                            <span className="button-spinner">⏳</span>
                        ) : (
                            <span className="send-icon">➤</span>
                        )}
                    </button>
                </div>
                <div className="input-hint">
                    Press <kbd>Enter</kbd> to send, <kbd>Shift + Enter</kbd> for new line
                </div>
            </form>
        </div>
    )
}

export default ChatInput
