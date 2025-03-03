import { useState, useEffect } from 'react';
import api from '../../api';
import profilepic from "./assets/profilepic.png";
import potpic from "./assets/potpic.png"; 
import applepic from "./assets/applepic.png";
import React from 'react';
import Navbar from "../../components/Navbar";  

const FridgeRecipePage = ({ userId, recipeId }) => {
  const [foods, setFoods] = useState([]);
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchRecipe() {
      try {
        const userId = 111;
        const response = await api.get(`core/get_food_list/?uid=${userId}`);
        const data = response.data.data; // Get the data from response
        console.log(data);

        // Check if the response contains foods and tags
        if (data && data.foods && data.tags) {
          setFoods(data.foods); // Set foods array
          setTags(data.tags); // Set tags array
        } else {
          setError("No food data found.");
        }
      } catch (err) {
        setError("Failed to fetch food.");
      } finally {
        setLoading(false);
      }
    }

    fetchRecipe();
  }, [userId, recipeId]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!foods.length) return <p>No foods available.</p>;

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Header */}
 
      <Navbar /> {/* Add Navbar here */}
 
      {/* Main content */}
      <main className="flex flex-1 gap-4 p-4">
        {/* Left Column */}
        <section className="flex-1 bg-white rounded-lg shadow p-4">
          <div className="relative">
            <input
              type="text"
              placeholder="Search your items..."
              className="border rounded-full py-2 pl-4 pr-10 w-full"
            />
            <button className="absolute right-2 top-2 text-gray-500">
              🔍
            </button>
          </div>
          <div className="mt-4 space-y-2">
            {foods.map((food, index) => (
              <div key={index} className="border rounded-lg flex items-center p-2 h-12">
                <span className="font-semibold">{food}</span>
                <img src="foodPicPlaceholder" alt={food} className="ml-auto h-10" /> {/* Use actual images if available */}
              </div>
            ))}
          </div>

          <button className="mt-4 bg-gray-800 text-white py-2 px-4 rounded-lg">
            Organize Fridge
          </button>
        </section>

        {/* Center Column */}
        <section className="flex-1 bg-white rounded-lg shadow p-4 flex flex-col items-center justify-center">
          <span className="inline-block bg-gray-800 text-white rounded px-2 py-1">
            {tags.length > 0 ? `Tag: ${tags[0]}` : 'No tags available'}
          </span>
          <img src={potpic} alt="pot" className="mt-4" />
        </section>

        {/* Right Column */}
        <section className="flex-1 bg-white rounded-lg shadow p-4">
          <input
            type="text"
            placeholder="Search flavor..."
            className="border rounded-full py-2 pl-4 w-full"
          />

          <div className="mt-4 flex flex-col gap-2">
            {tags.map((tag, index) => (
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
