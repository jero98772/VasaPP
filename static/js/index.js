const { useState } = React;

function Index() {
    const navigateTo = (path) => {
        window.location.href = path;
    };

    return (
        <div className="container index-container">
            <div className="logo">VassaPP</div>
            <div className="tagline">// End-to-End Encrypted Communication //</div>
            
            <div className="security-badge">
                🔒 MILITARY-GRADE ENCRYPTION
            </div>

            <div className="options">
                <div className="option-card" onClick={() => navigateTo('/auth/login')}>
                    <div className="option-icon">👤</div>
                    <div className="option-title">EXISTING USER</div>
                    <div className="option-description">
                        Login with your credentials.
                    </div>
                    <div style={{ marginTop: '1.5rem' }}>
                        <button className="btn">LOGIN</button>
                    </div>
                </div>

                <div className="option-card" onClick={() => navigateTo('/chat')}>
                    <div className="option-icon">💬</div>
                    <div className="option-title">ANONYMOUS CHAT</div>
                    <div className="option-description">
                        Start chatting immediately.
                    </div>
                    <div style={{ marginTop: '1.5rem' }}>
                        <button className="btn">START CHAT</button>
                    </div>
                </div>
            </div>
        </div>
    );
}

ReactDOM.render(<Index />, document.getElementById('root'));