import React, { useEffect, useState } from "react";
import api from '../../api';
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../../constants';

export default function RecipeDetail({ userId, recipeId }) {
  const [recipe, setRecipe] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchRecipe() {
      try {
        // const response = await api.get(`core/recipe_detail/?user_id=${userId}&recipe_id=${recipeId}`);
        const response = await api.get(
          `core/recipe_detail/?user_id=${userId}&recipe_id=${recipeId}`, 
          {
            headers: { Authorization: `Bearer ${localStorage.getItem(ACCESS_TOKEN)}` },
          }
        );
        const data = response.data.data.recipes;
        if (data && data.length > 0) {
          setRecipe(data[0]);
        } else {
          setError("No recipe found.");
        }
      } catch (err) {
        setError("Failed to fetch recipe.");
      } finally {
        setLoading(false);
      }
    }

    fetchRecipe();
  }, [userId, recipeId]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!recipe) return <p>No recipe available.</p>;

  return (
    <div className="min-h-screen bg-gray-100 flex justify-center py-10">
      <div className="bg-white shadow-lg rounded-lg p-6 max-w-4xl w-full">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-6">
          {recipe.name || "Unknown Recipe"}
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Ingredients Section */}
          <div className="border border-gray-300 rounded-lg p-4 bg-blue-50">
            <h2 className="text-xl font-semibold text-blue-900 mb-4">Ingredients</h2>
            <ul className="list-disc list-inside text-gray-600">
              {recipe.ingredients?.map((ingredient, index) => (
                <li key={index}>{ingredient}</li>
              )) || <p>No ingredients listed.</p>}
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
                <button className="bg-yellow-500 text-white px-4 py-2 rounded-lg shadow hover:bg-yellow-600">
                  Cook
                </button>
                <button className="bg-gray-700 text-white px-4 py-2 rounded-lg shadow hover:bg-gray-800">
                  Print
                </button>
              </div>
            </div>
            <ol className="space-y-4 text-gray-700">
              {recipe.steps?.map((step, index) => (
                <li key={index}><strong>{index + 1}.</strong> {step}</li>
              )) || <p>No steps provided.</p>}
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
}
