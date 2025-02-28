import React from 'react';

import { BrowserRouter as Router, Routes, Route, Link, Navigate, BrowserRouter } from 'react-router-dom';
<<<<<<< HEAD

=======
 
 
>>>>>>> 69ece60558087e139de7cb7eb5fecb06e9f05859
import SignUp from './components/SignupLogin/SignUp';
import Profile from './components/Profile/Profile';
import Login from './components/SignupLogin/Login';
import ProtectedRoute from './components/ProtectedRoute';
import NotFound from './components/NotFound/NotFound';
 
import Fridge from "./components/Fridge/Fridge"; 
import RecipeDetail from "./components/RecipeDetail/RecipeDetail";  
 
import Fridge from "./components/Fridge/Fridge";
<<<<<<< HEAD

import RecipeGen from './components/RecipeGenerate/RecipeGen'


=======
 
import Recipe from './components/Recipe/Recipe'
  
>>>>>>> 69ece60558087e139de7cb7eb5fecb06e9f05859
function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <SignUp />;
}

function App() {
  return (
    <Router>
      <Routes> 
        <Route path="/" element={<Navigate to="/login" replace />} />

        <Route path="/signup" element={<RegisterAndLogout />} />
        <Route path="/login" element={<Login />} />
<<<<<<< HEAD
        <Route path="/logout" element={<Logout />} />

        <Route path="/profile" element={<ProtectedRoute><Profile></Profile></ProtectedRoute>} />
        <Route path="/fridge" element={<Fridge />} />
        <Route path="/recipe_gen" element={<RecipeGen />} />

=======
        <Route path="/logout" element={<Logout />} /> 
        <Route path="/profile" element={<ProtectedRoute><Profile></Profile></ProtectedRoute>} />
        <Route path="/fridge" element={<Fridge />} />  
        <Route path="/RecipeDetail" element={<ProtectedRoute><Recipe></RecipeDetail></ProtectedRoute>} />  
 
        <Route path="/recipe" element={<Recipe />} />
  
>>>>>>> 69ece60558087e139de7cb7eb5fecb06e9f05859
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
}

export default App;
