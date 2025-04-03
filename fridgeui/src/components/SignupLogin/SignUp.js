import React, { useState } from 'react';
import api from '../../api';
import './signuplogin.css';
import { useNavigate } from 'react-router-dom';

function SignUp() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    username: ''
  });
  const [loading, setLoading] = useState(false); // avoid duplicate send

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (loading) return; // avoid duplicate lick

    setLoading(true);
    try {
      await api.post('/core/register/', formData);
      alert('Sign Up Successful!');
      navigate('/login');
    } catch (err) {
      console.error(err);
      alert('Sign Up Failed!'+err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bodybox">
      <div className="auth-container">
        <div className="auth-box">
          <h1 className="auth-title">Hello!</h1>

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
              placeholder="Enter your email"
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
              placeholder="Enter your password"
            />

            <label className="auth-label" htmlFor="username">USERNAME</label>
            <input
              id="username"
              type="text"
              name="username"
              className="auth-input"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="Enter your username"
            />

            <button type="submit" className="auth-button" disabled={loading}>
              {loading ? 'Signing up...' : 'Sign up'}
            </button>
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
