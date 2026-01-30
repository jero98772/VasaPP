const { useState, useEffect, useRef } = React;

function Chat() {
    const [messages, setMessages] = useState([
        {
            id: 1,
            text: 'Welcome to Secure Chat. Your messages are end-to-end encrypted.',
            type: 'received',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
    ]);
    const [inputMessage, setInputMessage] = useState('');
    const [username] = useState('User_' + Math.floor(Math.random() * 10000));
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = (e) => {
        e.preventDefault();
        
        if (inputMessage.trim() === '') return;

        const newMessage = {
            id: messages.length + 1,
            text: inputMessage,
            type: 'sent',
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };

        setMessages(prev => [...prev, newMessage]);
        setInputMessage('');

        // Simulate receiving a response
        setTimeout(() => {
            const responseMessage = {
                id: messages.length + 2,
                text: 'Message received and encrypted.',
                type: 'received',
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
            };
            setMessages(prev => [...prev, responseMessage]);
        }, 1000);
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage(e);
        }
    };

    const handleLogout = () => {
        if (confirm('Are you sure you want to exit secure chat?')) {
            window.location.href = '/';
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-header">
                <div>
                    <div className="chat-title">SECURE_CHAT // ENCRYPTED</div>
                    <div style={{ fontSize: '0.85rem', color: 'var(--text-gray)', marginTop: '0.25rem' }}>
                        {username}
                    </div>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '2rem' }}>
                    <div className="chat-status">
                        <span className="status-indicator"></span>
                        <span>SECURE CONNECTION</span>
                    </div>
                    <button className="btn btn-secondary" onClick={handleLogout} style={{ padding: '8px 20px', fontSize: '0.85rem' }}>
                        EXIT
                    </button>
                </div>
            </div>

            <div className="chat-messages">
                {messages.map((message) => (
                    <div 
                        key={message.id} 
                        className={`message ${message.type === 'sent' ? 'message-sent' : 'message-received'}`}
                    >
                        <div className="message-text">{message.text}</div>
                        <span className="message-time">{message.time}</span>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSendMessage} className="chat-input-container">
                <input
                    type="text"
                    className="chat-input"
                    placeholder="Type your encrypted message..."
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                />
                <button type="submit" className="send-btn">
                    SEND
                </button>
            </form>
        </div>
    );
}

ReactDOM.render(<Chat />, document.getElementById('root'));