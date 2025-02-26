import React, { useState } from 'react';
import axios from 'axios';
import './signuplogin.css';

function SignUp() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: ''
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
      await axios.post('http://127.0.0.1:8000/demo/register/', formData);
      alert('Sign Up Successful!');
    } catch (err) {
      console.error(err);
      alert('Sign Up Failed!');
    }
  };

  return (
    <div className="bodybox">
    <div className="auth-container">
      <div className="auth-box">
        <h1 className="auth-title">Hello!</h1>

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

          <label className="auth-label">USERNAME</label>
          <input
            type="text"
            name="username"
            className="auth-input"
            value={formData.username}
            onChange={handleChange}
            required
          />

          <button type="submit" className="auth-button">Sign up</button>
        </form>

        <div className="auth-links">
          <a href="/signup" className="auth-link active">Sign up</a>
          <a href="/login" className="auth-link">Log in</a>
        </div>
      </div>
    </div>
    </div>
  );
}

export default SignUp;
