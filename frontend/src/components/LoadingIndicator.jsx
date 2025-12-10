import './LoadingIndicator.css'

function LoadingIndicator() {
    return (
        <div className="loading-indicator">
            <div className="loading-avatar">🤖</div>
            <div className="loading-content">
                <div className="loading-dots">
                    <span className="dot"></span>
                    <span className="dot"></span>
                    <span className="dot"></span>
                </div>
                <span className="loading-text">AI is thinking...</span>
            </div>
        </div>
    )
}

export default LoadingIndicator
