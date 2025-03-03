// src/components/Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import { RxAvatar } from "react-icons/rx";

const Navbar = () => {
  const userId = localStorage.getItem("user_id");
  const profilePic = localStorage.getItem("profile_pic")
  return (
    <nav className="flex justify-between items-center px-8 py-4 shadow-sm">
      <span className="font-bold text-xl">eFridge</span>
      <ul className="flex gap-6">
        <li>
          {/* go to /recipe  */}
          <Link to="/recipe_gen" className='hover:underline'>RECIPE</Link>
        </li>
        <li>
          {/* go to /fridge */}
          <Link to="/fridge" className='hover:underline'>FRIDGE</Link>
        </li>
        <li>
          {/* go to /profile  */}
          <Link to="/profile" className='hover:underline'>PROFILE</Link>
        </li>
      </ul>
      <div className="flex items-center gap-4">
        {/* Profile Avatar */}
        {userId ? (
          <Link to="/profile">
            {profilePic ? (
              <img
                className="rounded-full h-10 w-10 object-cover border-2 border-gray-300"
                src={profilePic}
                alt="Profile"
              />
            ) : (
              <RxAvatar className="h-10 w-10 text-gray-500 hover:text-green-500" />
            )}
          </Link>
        ) : null}

        {/* Logout Button */}
        <Link
          to="/logout"
          className=" text-black px-3 py-1 rounded-md text-sm hover:text-red-600"
        >
          Logout
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
