import './ChatMessage.css'

function ChatMessage({ role, content, timestamp }) {
    const isUser = role === 'user'

    const formatTime = (isoString) => {
        const date = new Date(isoString)
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        })
    }

    return (
        <div className={`message ${isUser ? 'message-user' : 'message-assistant'}`}>
            <div className="message-avatar">
                {isUser ? '👤' : '🤖'}
            </div>
            <div className="message-content-wrapper">
                <div className="message-header">
                    <span className="message-role">{isUser ? 'You' : 'AI Assistant'}</span>
                    <span className="message-timestamp">{formatTime(timestamp)}</span>
                </div>
                <div className="message-content">
                    {content}
                </div>
            </div>
        </div>
    )
}

export default ChatMessage
