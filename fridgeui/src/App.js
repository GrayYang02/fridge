import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, BrowserRouter} from 'react-router-dom';
import SignUp from './components/SignupLogin/SignUp';
import Profile from './components/Profile/Profile';
import Login from './components/SignupLogin/Login';
import ProtectedRoute from './components/ProtectedRoute';
import NotFound from './components/NotFound/NotFound';

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />;
} 

function RegisterAndLogout() {
  localStorage.clear()
  return <SignUp />;
}

function App() {
  return (
    <Router>
      {/* <nav style={{ margin: '1rem' }}>
        <Link to="/signup" style={{ marginRight: '1rem' }}>Sign up</Link>
        <Link to="/login">Log in</Link>
      </nav> */}

      <Routes>
        <Route path="/signup" element={<RegisterAndLogout />} />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/profile" element={<ProtectedRoute><Profile></Profile></ProtectedRoute> } />
        <Route path="*" element={<NotFound />} />
        {/* 你也可以加其它页面路由 */}
      </Routes>
    </Router>
  );
}

export default App;


