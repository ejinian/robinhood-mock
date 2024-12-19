import React, { useState } from 'react';
import axios from 'axios';

function Register() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:5000/register', { username, password });
            alert('Registration Successful');
        } catch (error) {
            alert('Registration Failed');
        }
    };

    return (
        <div className="container mt-5">
            <form onSubmit={handleRegister} className="card card-body bg-light">
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
                <button type="submit" className="btn btn-primary mt-3">Register</button>
            </form>
        </div>
    );
}

export default Register;
