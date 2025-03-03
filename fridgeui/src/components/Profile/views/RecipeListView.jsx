import React, { useEffect, useState, useContext } from "react";
import recipepic from "../assets/recipepic.png";
import api from "../../../api";
import { UserContext } from "./UserProvider";
import Pagination from "../../Pagination/Pagination";

const RecipeListView = ({ title, operationName }) => {
  const { userinfo } = useContext(UserContext);
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [collectedRecipes, setCollectedRecipes] = useState(new Set());
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const opmap = {
    cooked: 1,
    collected: 2,
    viewed: 3,
  };

  useEffect(() => {
    const fetchRecipes = async () => {
      if (!userinfo?.id) return; // Ensure userinfo is loaded

      try {
        const response = await api.get(`/core/user-recipe-log/`, {
          params: {
            userid: userinfo.id,
            op: opmap[operationName],
            page: currentPage,
            page_size: 1,
          },
        });

        if (response.status !== 200) throw new Error("Failed to fetch recipes");

        setRecipes(response.data.results);
        setTotalPages(response.data.count);
      } catch (err) {
        console.error("Error fetching recipes:", err);
        setError("Failed to load recipes");
      } finally {
        setLoading(false);
      }
    };

    fetchRecipes();
  }, [userinfo, operationName, currentPage]);

  useEffect(() => {
    const fetchCollectedRecipes = async () => {
      if (!userinfo?.id) return;

      try {
        const response = await api.get(`/core/user-recipe-log/`, {
          params: {
            userid: userinfo.id,
            op: 2, // 2 is the operation number for collected recipes
            page_size: 9999,
            page: 1,
          },
        });

        if (response.status !== 200)
          throw new Error("Failed to fetch collected recipes");
        console.log(response.data);

        const collectedSet = new Set(
          response.data.results.map((entry) => entry.recipe_details.id)
        ); // Store collected recipe IDs
        setCollectedRecipes(collectedSet);
      } catch (err) {
        console.error("Error fetching collected recipes:", err);
      }
    };

    fetchCollectedRecipes();
  }, [userinfo]);

  const toggleCollected = async (recipeId) => {
    try {
      const isCurrentlyCollected = collectedRecipes.has(recipeId);

      if (isCurrentlyCollected) {
        await api.post(`/core/user-recipe-log/toggle-log/`, {
          userid: userinfo.id,
          recipe_id: recipeId,
          op: 2,
        });
        setCollectedRecipes((prev) => {
          const newSet = new Set(prev);
          newSet.delete(recipeId);
          return newSet;
        });
      } else {
        await api.post(`/core/user-recipe-log/toggle-log/`, {
          userid: userinfo.id,
          recipe_id: recipeId,
          op: 2,
        });
        setCollectedRecipes((prev) => new Set(prev).add(recipeId));
      }
    } catch (error) {
      console.error("Error toggling collection status:", error);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <>
      <h1 className="text-xl font-bold mb-4">{title}</h1>
      <div className="space-y-4">
        {recipes.length === 0 ? (
          <p>No recipes found.</p>
        ) : (
          recipes.map((recipe) => (
            <div
              key={recipe.id}
              className="flex items-center bg-gray-50 rounded-lg p-4 shadow-sm"
            >
              {/* Recipe pic */}
              <img
                className="w-20 h-20 rounded-lg"
                src={recipepic}
                alt="RecipePic"
              />

              {/* Recipe info */}
              <div className="ml-4 flex-1">
                <div className="flex flex-row justify-between">
                  <h2 className="font-semibold text-lg">
                    {recipe.recipe_details.recipe_name}
                  </h2>
                  <button
                    className={`text-xl ${
                      collectedRecipes.has(recipe.recipe_details.id)
                        ? "text-yellow-500"
                        : "text-gray-400"
                    }`}
                    onClick={() => toggleCollected(recipe.recipe_details.id)}
                  >
                    ★
                  </button>
                </div>
                <div className="flex">
                  <p className="text-lg text-gray-500">Required Food:</p>
                </div>
                <div className="flex gap-2 mt-1">
                  {recipe.recipe_details.food?.split(",").map((food, index) => (
                    <span
                      key={index}
                      className="bg-black text-white px-2 py-1 text-xs rounded"
                    >
                      {food}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))
        )}
      </div>
      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={setCurrentPage}
      ></Pagination>
    </>
  );
};

export default RecipeListView;
