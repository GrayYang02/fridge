import React from 'react';
import Navbar from './components/Navbar';

import { BrowserRouter as Router, Routes, Route, Link, Navigate, BrowserRouter } from 'react-router-dom';

import SignUp from './components/SignupLogin/SignUp';
import Profile from './components/Profile/Profile';
import Login from './components/SignupLogin/Login';
import ProtectedRoute from './components/ProtectedRoute';
import NotFound from './components/NotFound/NotFound';
import Fridge from "./components/Fridge/Fridge";




import { UserProvider } from './components/Profile/views/UserProvider';



import RecipeGen from './components/RecipeGenerate/RecipeGen'
import RecipeDetail from './components/RecipeDetail/RecipeDetail'


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
        {/* Default redirect to login page */}

        <Route path="/" element={<Navigate to="/login" replace />} />

        {/* Pages that do NOT require the navbar */}
        <Route path="/signup" element={<RegisterAndLogout />} />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />

        {/* Pages that require the common navbar */}



        <Route path="/profile" element={<ProtectedRoute><UserProvider><Profile /></UserProvider></ProtectedRoute>} />
        <Route path="/fridge" element={<ProtectedRoute><UserProvider><Fridge /></UserProvider></ProtectedRoute>} />
        <Route path="/recipe_gen" element={<ProtectedRoute><UserProvider><RecipeGen /></UserProvider></ProtectedRoute>} />

=

        {/* <Route path="/recipe_detail" element={<RecipeDetail userId={121} recipeId={10} />} /> */}

        <Route path="*" element={<NotFound />} />
      </Routes>

    </Router>
  );
}


export default App;
