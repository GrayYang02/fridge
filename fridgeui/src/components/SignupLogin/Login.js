import React, { useState } from 'react';
import api from '../../api';
import './signuplogin.css';
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../../constants';


function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/core/token/', formData);
      localStorage.setItem(ACCESS_TOKEN, response.data.access);
      localStorage.setItem(REFRESH_TOKEN, response.data.refresh);

      navigate('/profile');

    } catch (err) {
      console.error(err);
      alert('Login Failed!');
    }
  };

  return (
    <div className="bodybox">
    <div className="auth-container">
      <div className="auth-box">
        <h1 className="auth-title">Welcome back!</h1>

        <form onSubmit={handleSubmit} className="auth-form">
          <label className="auth-label" htmlFor="email">EMAIL</label>
          <input
            id="email"  
            type="email"
            name="email"
            className="auth-input"
            value={formData.email}
            onChange={handleChange}
            required
          />

          <label className="auth-label" htmlFor="password">PASSWORD</label>
          <input
            id="password"
            type="password"
            name="password"
            className="auth-input"
            value={formData.password}
            onChange={handleChange}
            required
          />

          <button type="submit" className="auth-button">Log in</button>
        </form>

        <div className="auth-links">
          <a href="/signup" className="auth-link">Sign up</a>
          <a href="/login" className="auth-link active">Log in</a>
        </div>
      </div>
    </div>
    </div>
  );
}

export default Login;
