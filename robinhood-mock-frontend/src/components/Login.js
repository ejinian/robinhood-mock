import React, { useState } from 'react';
import axios from 'axios';

function Login({ onLogin }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/login', {
                username,
                password
            }, {
                withCredentials: true
            });
            onLogin();
            console.log('Login successful:', response.data);
        } catch (error) {
            console.error('Login failed:', error.response ? error.response.data : error);
            alert('Login Failed');
        }
    };
    
    return (
        <div className="container mt-5">
            <form onSubmit={handleLogin} className="card card-body bg-light">
                <div className="form-group">
                    <label htmlFor="username">Username:</label>
                    <input
                        type="text"
                        className="form-control"
                        id="username"
                        value={username}
                        onChange={e => setUsername(e.target.value)}
                        placeholder="Enter your username"
                    />
                </div>
                <div className="form-group mt-3">
                    <label htmlFor="password">Password:</label>
                    <input
                        type="password"
                        className="form-control"
                        id="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                        placeholder="Enter your password"
                    />
                </div>
                <button type="submit" className="btn btn-primary mt-3">Login</button>
            </form>
        </div>
    );
}

export default Login;
