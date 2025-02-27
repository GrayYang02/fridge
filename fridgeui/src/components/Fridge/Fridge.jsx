import React, { useState, useEffect } from 'react';
import { fetchFridgeItems } from '../../api';

const FridgePage = () => {
  const [fridgeItems, setFridgeItems] = useState([]);
  const [expiringItems, setExpiringItems] = useState([]);

  useEffect(() => {
    const loadItems = async () => {
      const items = await fetchFridgeItems();
      const now = new Date();

      const expiring = items.filter(item => new Date(item.expire_time) <= new Date(now.getTime() + 3 * 24 * 60 * 60 * 1000));
      const stored = items.filter(item => !expiring.includes(item));
      
      setExpiringItems(expiring);
      setFridgeItems(stored);
    };

    loadItems();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <nav className="flex justify-between items-center px-8 py-4 shadow-sm">
        <span className="font-bold text-xl">APPNAME</span>
        <ul className="flex gap-6">
          <li>RECIPE</li>
          <li className="font-semibold">FRIDGE</li>
          <li>PROFILE</li>
        </ul>
        <div>
          <img
            className="rounded-full h-12 w-12 object-cover"
            src="https://placehold.co/100x100"
            alt="User"
          />
        </div>
      </nav>

      <main className="p-8">
        <section className="flex gap-4">
          <div className="bg-white p-4 shadow rounded-lg w-60">
            <h3 className="font-semibold text-red-500">Expired/Expiring Soon</h3>
            <ul className="mt-4 space-y-3 overflow-y-auto max-h-60">
              {expiringItems.map((item) => (
                <li key={item.id} className="flex items-center gap-2 border-b pb-2">
                  <span className="text-red-500">{item.name}</span>
                  <img src={item.pic || "https://placehold.co/50x50/png"} alt={item.name} className="h-8 w-8" />
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-white p-4 shadow rounded-lg flex-grow">
            <div className="flex items-center gap-2 mb-4">
              <input className="border rounded-lg px-2 py-1 flex-grow" placeholder="Search ingredients" />
              <select className="border rounded-lg px-2 py-1">
                <option>Meat and Vegetable</option>
              </select>
            </div>

            <div className="border rounded-lg p-4 relative bg-gray-100">
              <div className="grid grid-cols-5 gap-2">
                {fridgeItems.map((item) => (
                  <div key={item.id} className="bg-white flex flex-col items-center p-2 shadow rounded-lg relative">
                    <button className="absolute top-1 left-1 text-xs">✕</button>
                    <img src={item.pic || "https://placehold.co/50x50/png"} alt={item.name} />
                    <span>{item.name}</span>
                  </div>
                ))}
              </div>
            </div>

            <button className="mt-6 bg-brown-500 text-white py-2 px-6 rounded-lg">
              Add ingredients
            </button>
          </div>
        </section>
      </main>
    </div>
  );
};

export default FridgePage;
