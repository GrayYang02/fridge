import React, { useEffect, useState } from "react";
import api from '../../api';

import { useParams, useLocation } from "react-router-dom";

const RecipePage = () => {
  const [recipe, setRecipe] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Get the user_id from the URL
  const { user_id } = useParams();
  
  // You can also use query parameters using useLocation hook
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const userIdFromQuery = queryParams.get('user_id');

  useEffect(() => {
    const fetchRecipe = async () => {
      try {
        // Use user_id (from either path or query) to fetch data
        const recipe_id = 1;
        const response = await api.get(`demo/recipe_detail/?user_id = ${userIdFromQuery}& recipe_id=${recipe_id}`);
        setRecipe(response.data.recipe);
        console.log(response.data.recipe)
        setLoading(false);
      } catch (err) {
        setError("Failed to fetch recipe");
        setLoading(false);
      }
    };

    fetchRecipe();
  }, [user_id, userIdFromQuery]); // Dependency array to refetch if user_id changes

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center py-10">
      <div className="bg-white shadow-lg rounded-lg p-6 max-w-4xl w-full">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-6">
          { setRecipe.name}
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Ingredients Section */}
          <div className="border border-gray-300 rounded-lg p-4 bg-blue-50">
            <h2 className="text-xl font-semibold text-blue-900 mb-4">Ingredients</h2>
            <ul className="list-disc list-inside text-gray-600 mb-4">
              { setRecipe.ingredients}
            </ul>

            
          </div>

          {/* Directions Section */}
          <div className="md:col-span-2">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-800">Directions</h2>
              <div className="flex space-x-4">
                <button className="bg-green-500 text-white px-4 py-2 rounded-lg shadow hover:bg-green-600">
                  Save
                </button>
                <button className="bg-gray-700 text-white px-4 py-2 rounded-lg shadow hover:bg-gray-800">
                  Print
                </button>
              </div>
            </div>
            <ol className="space-y-4 text-gray-700">
              {recipe?.directions?.map((direction, index) => (
                <li key={index}><strong>{index + 1}.</strong> {direction}</li>
              ))}
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipePage;
