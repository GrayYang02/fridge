import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import SignUp from './components/SignupLogin/SignUp';
import Profile from './components/Profile/Profile';
import Login from './components/SignupLogin/Login';

function App() {
  return (
    <Router>
      <nav style={{ margin: '1rem' }}>
        <Link to="/signup" style={{ marginRight: '1rem' }}>Sign up</Link>
        <Link to="/login">Log in</Link>
      </nav>

      <Routes>
        <Route path="/signup" element={<SignUp />} />
        <Route path="/login" element={<Login />} />
        <Route path="/profile" element={<Profile />} />
        {/* 你也可以加其它页面路由 */}
      </Routes>
    </Router>
  );
}

export default App;


