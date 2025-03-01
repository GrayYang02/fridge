// src/components/Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="flex justify-between items-center px-8 py-4 shadow-sm">
      <span className="font-bold text-xl">APPNAME</span>
      <ul className="flex gap-6">
        <li>
          {/* 这里跳转到 /recipe 路由 */}
          <Link to="/recipe">RECIPE</Link>
        </li>
        <li>
          {/* 跳转到 /fridge 路由 */}
          <Link to="/fridge">FRIDGE</Link>
        </li>
        <li>
          {/* 跳转到 /profile 路由 */}
          <Link to="/profile">PROFILE</Link>
        </li>
      </ul>
      <div>
        <img
          className="rounded-full h-12 w-12 object-cover"
          src="https://placehold.co/100x100"
          alt="User"
        />
      </div>
    </nav>
  );
};

export default Navbar;
