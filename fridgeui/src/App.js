import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import Navbar from './components/Navbar';
import SignUp from './components/SignupLogin/SignUp';
import Profile from './components/Profile/Profile';
import Login from './components/SignupLogin/Login';
import ProtectedRoute from './components/ProtectedRoute';
import NotFound from './components/NotFound/NotFound';
import Fridge from "./components/Fridge/Fridge";
import Recipe from './components/Recipe/Recipe';

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <SignUp />;
}

// Common layout: includes Navbar and nested routes
const LayoutWithNavbar = () => (
  <>
    <Navbar />
    <Outlet />
  </>
);

function App() {
  return (
    <Router>
      <Routes>
        {/* Default redirect to login page */}
        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Pages that do NOT require the navbar */}
        <Route path="/signup" element={<RegisterAndLogout />} />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />

        {/* Pages that require the common navbar */}
        <Route element={<LayoutWithNavbar />}>
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="/fridge" element={<Fridge />} />
          <Route path="/recipe" element={<Recipe />} />
        </Route>

        {/* 404 page */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
