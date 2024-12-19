import React from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';

function Navbar({ isLoggedIn, onLogout }) {
    const handleLogout = async () => {
        try {
            await axios.get('http://localhost:5000/logout', { withCredentials: true });
            onLogout();
        } catch (error) {
            console.error('Failed to log out:', error);
        }
    };

    return (
        <nav style={{ backgroundColor: '#086434', padding: '10px', color: 'white' }}>
            <Link to="/" style={{ color: 'white', marginRight: '10px' }}>Home</Link>
            {!isLoggedIn ? (
                <>
                    <Link to="/register" style={{ color: 'white', marginRight: '10px' }}>Register</Link>
                    <Link to="/login" style={{ color: 'white', marginRight: '10px' }}>Login</Link>
                </>
            ) : (
                <button onClick={handleLogout} style={{ color: 'white', background: 'none', border: 'none' }}>Logout</button>
            )}
        </nav>
    );
}

export default Navbar;
