const { useState } = React;

function Login() {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        
        if (isLogin) {
            // Handle login
            console.log('Login:', formData);
            // Redirect to chat after successful login
            window.location.href = '/chat';
        } else {
            // Handle registration
            if (formData.password !== formData.confirmPassword) {
                alert('Passwords do not match!');
                return;
            }
            console.log('Register:', formData);
            // Redirect to chat after successful registration
            window.location.href = '/chat';
        }
    };

    const toggleMode = () => {
        setIsLogin(!isLogin);
        setFormData({
            username: '',
            email: '',
            password: '',
            confirmPassword: ''
        });
    };

    return (
        <div className="container">
            <div className="auth-container">
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <div className="logo" style={{ fontSize: '2.5rem' }}>VassaPP
Change this is not valid
                    </div>
                </div>

                <div className="form-card">
                    <div className="form-header">
                        <h2 className="form-title">
                            {isLogin ? '// ACCESS TERMINAL //' : '// CREATE ACCOUNT //'}
                        </h2>
                        <p className="form-subtitle">
                            {isLogin 
                                ? 'Enter your credentials to access secure chat' 
                                : 'Register for encrypted communication'}
                        </p>
                    </div>

                    <form onSubmit={handleSubmit}>
                        {!isLogin && (
                            <div className="form-group">
                                <label className="form-label" htmlFor="username">USERNAME</label>
                                <input
                                    type="text"
                                    id="username"
                                    name="username"
                                    className="form-input"
                                    placeholder="enter_username"
                                    value={formData.username}
                                    onChange={handleInputChange}
                                    required={!isLogin}
                                />
                            </div>
                        )}

                        <div className="form-group">
                            <label className="form-label" htmlFor="email">EMAIL</label>
                            <input
                                type="email"
                                id="email"
                                name="email"
                                className="form-input"
                                placeholder="user@secure.net"
                                value={formData.email}
                                onChange={handleInputChange}
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label className="form-label" htmlFor="password">PASSWORD</label>
                            <input
                                type="password"
                                id="password"
                                name="password"
                                className="form-input"
                                placeholder="••••••••••"
                                value={formData.password}
                                onChange={handleInputChange}
                                required
                            />
                        </div>

                        {!isLogin && (
                            <div className="form-group">
                                <label className="form-label" htmlFor="confirmPassword">CONFIRM PASSWORD</label>
                                <input
                                    type="password"
                                    id="confirmPassword"
                                    name="confirmPassword"
                                    className="form-input"
                                    placeholder="••••••••••"
                                    value={formData.confirmPassword}
                                    onChange={handleInputChange}
                                    required={!isLogin}
                                />
                            </div>
                        )}

                        <button type="submit" className="btn" style={{ width: '100%', marginTop: '1rem' }}>
                            {isLogin ? 'LOGIN' : 'REGISTER'}
                        </button>
                    </form>

                    <div className="form-footer">
                        <p>
                            {isLogin ? "Don't have an account? " : "Already have an account? "}
                            <span className="form-link" onClick={toggleMode}>
                                {isLogin ? 'Register here' : 'Login here'}
                            </span>
                        </p>
                    </div>

                    {isLogin && (
                        <div className="form-footer" style={{ marginTop: '1rem' }}>
                            <span className="form-link">Forgot password?</span>
                        </div>
                    )}
                </div>

                <div style={{ textAlign: 'center', marginTop: '2rem' }}>
                    <a href="/" className="btn btn-secondary">← BACK TO HOME</a>
                </div>
            </div>
        </div>
    );
}

ReactDOM.render(<Login />, document.getElementById('root'));