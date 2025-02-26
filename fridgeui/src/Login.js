import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

function Login() {
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
      const response = await axios.post('http://127.0.0.1:8000/demo/login/', formData);
      const { token } = response.data;
      localStorage.setItem('token', token);
      alert('Login Successful!');
    } catch (err) {
      console.error(err);
      alert('Login Failed!');
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h1 className="auth-title">Welcome back!</h1>

        <form onSubmit={handleSubmit} className="auth-form">
          <label className="auth-label">EMAIL</label>
          <input
            type="email"
            name="email"
            className="auth-input"
            value={formData.email}
            onChange={handleChange}
            required
          />

          <label className="auth-label">PASSWORD</label>
          <input
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
  );
}

export default Login;
