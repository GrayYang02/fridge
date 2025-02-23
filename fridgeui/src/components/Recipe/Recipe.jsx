import profilepic from "./assets/profilepic.png";
import potpic from "./assets/potpic.png";
import React from 'react';

const FridgeRecipePage = () => {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Header */}
      <header className="flex justify-between items-center p-4 bg-white shadow">
        <h1 className="text-xl font-semibold">APPNAME</h1>
        <nav className="flex gap-6">
          <span className="cursor-pointer">RECIPE</span>
          <span className="cursor-pointer">FRIDGE</span>
          <span className="cursor-pointer">PROFILE</span>
        </nav>
        <img
          className="w-24 h-24 rounded-full border-4 border-gray-300"
          src={profilepic}
          alt="ProfilePic"
        />
      </header>

      {/* Main content */}
      <main className="flex flex-1 gap-4 p-4">
        {/* Left Column */}
        <section className="flex-1 bg-white rounded-lg shadow p-4">
          <div className="relative">
            <input
              type="text"
              placeholder="text"
              className="border rounded-full py-2 pl-4 pr-10 w-full"
            />
            <button className="absolute right-2 top-2 text-gray-500">
              🔍
            </button>
          </div>

          <div className="mt-4 space-y-2">
            <div className="border rounded-lg flex items-center p-2">
              <span className="font-semibold">apple</span>
              <img src="https://placehold.co/50x50" alt="apple" className="ml-auto" />
            </div>
            <div className="border rounded-lg flex items-center p-2">
              <span className="font-semibold">apple</span>
              <img src="https://placehold.co/50x50" alt="apple" className="ml-auto" />
            </div>
          </div>

          <button className="mt-4 bg-gray-800 text-white py-2 px-4 rounded-lg">
            organize fridge
          </button>
        </section>

        {/* Center Column */}
        <section className="flex-1 bg-white rounded-lg shadow p-4 flex flex-col items-center justify-center">
          <div className="border rounded-lg flex items-center p-2 mb-4">
            <span className="font-semibold">apple</span>
            <img src="https://placehold.co/50x50" alt="apple" className="ml-auto" />
          </div>
          <span className="inline-block bg-gray-800 text-white rounded px-2 py-1">
            sweet & sour
          </span>
          <img src={potpic} alt="pot" className="mt-4" />
        </section>

        {/* Right Column */}
        <section className="flex-1 bg-white rounded-lg shadow p-4">
          <input
            type="text"
            placeholder="Hinted search text"
            className="border rounded-full py-2 pl-4 w-full"
          />

          <div className="mt-4 flex flex-col gap-2">
            {['spice', 'sweet & sour', 'sweet', 'sour'].map((tag) => (
              <span
                key={tag}
                className="inline-block bg-gray-800 text-white rounded px-2 py-1"
              >
                {tag}
              </span>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
};

export default FridgeRecipePage;