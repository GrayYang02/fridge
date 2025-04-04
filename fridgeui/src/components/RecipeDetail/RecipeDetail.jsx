import React, { useEffect, useState } from "react";
import api from '../../api';
 
export default function RecipeDetail({ userId, recipeId, onClose}) {

const [recipe, setRecipe] = useState([]);
const [ingredient, setIngredient] = useState([])
const [recipeName, setRecipeName] = useState("")
const [error, setError] = useState(null);
const [loading, setLoading] = useState(true);
const [isCollected, setIsCollected] = useState(false);
const [calories, setCalories] = useState(0);
const [missingItems, setMissingItems] = useState([]);
const [listLoading, setListLoading] = useState(false); // for shopping list

const getShoppingList = async () => {
  setListLoading(true);
  setError("");
  try {
    const response = await api.get("/core/shopping_list/", {
      params: {
        userid: userId,
        recipe_id: recipeId,
      },
    });

    if (response.status === 200) {
      setMissingItems(response.data.data || []);
    } else {
      setError("Failed to fetch shopping list.");
    }
  } catch (err) {
    setError("Error: " + err.message);
  } finally {
    setListLoading(false);
  }
};

// const handleCreateViewRecord = async () => {
//   try {
//     await api.post(`/core/user-recipe-log/toggle-log/`, {
//       userid: userId,
//       recipe_id: recipeId,
//       op: 3,
//     });
//   } catch (error) {
//     console.error("Failed to create view record:", error);
//   }

// }
// useEffect(()=> {
//   async function createViewRecord() {
//     try {
//       await api.post(`/core/user-recipe-log/toggle-log/`, {
//         userid: userId,
//         recipe_id: recipeId,
//         op: 3,
//       });
//     } catch (error) {
//       console.error("Failed to create view record:", error);
//     }
//   }
//   createViewRecord()
// }, [recipeId])

  // Check if the recipe is collected
  useEffect(() => {
    async function checkCollected() {
      try {
        const response = await api.get(`/core/user-recipe-log/is_collected`, {
          params: { userid: userId, recipe_id: recipeId },
        });

        if (response.status === 200) {
          setIsCollected(response.data.is_collected);
        }
      } catch (error) {
        console.error("Failed to check collection status:", error);
      }
    }

    if (recipeId) checkCollected();
  }, [userId, recipeId]);

  // Toggle Recipe Collection
  const handleToggleCollection = async () => {
    try {
      await api.post(`/core/user-recipe-log/toggle-log/`, {
        userid: userId,
        recipe_id: recipeId,
        op: 2, // 2 means collected
      });

      setIsCollected((prev) => !prev);
    } catch (error) {
      console.error("Failed to toggle collection:", error);
    }
  };

  // Mark Recipe as Cooked
  const handleCook = async () => {
    try {
      await api.post(`/core/user-recipe-log/toggle-log/`, {
        userid: userId,
        recipe_id: recipeId,
        op: 1, // 1 means cooked
      });

      alert("Recipe marked as cooked!");
    } catch (error) {
      console.error("Failed to log cooked recipe:", error);
    }
  };

useEffect(() => {
  async function fetchRecipe() {
    try {
      const response = await api.get(`/core/recipe_detail/`, {
        params: { user_id: userId, id: recipeId },
      });

      if (response.status!==200){
        throw new Error("Failed to fetch");
      }

      console.log("response", response)

      
    
        setRecipe(JSON.parse(response.data.data.recipe.replace(/'/g, '"')));
        setIngredient(JSON.parse(response.data.data.food.replace(/'/g, '"')))
        setRecipeName(response.data.data.recipe_name)
        const caloriesValue = response.data.data.calories;
        console.log("calories", caloriesValue)
        if (caloriesValue !== "" && caloriesValue !== null && caloriesValue !== undefined) {
          setCalories(caloriesValue);
        }

      
      
    } catch (err) {
      setError("Failed to fetch recipe.");
    } finally {
      setLoading(false);
    }
  }

  if (recipeId) fetchRecipe();
}, [userId, recipeId]);

useEffect (() => {
  console.log("recipe", recipe)
  console.log("ingre", ingredient)
  console.log("name", recipeName)

}, [recipe, ingredient, recipeName]) 

if (!recipeId) return null; // Don't render modal if no recipe is selected

return (
  <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div className="relative bg-white rounded-lg shadow-lg max-w-3xl w-full max-h-[90vh] overflow-hidden">
      <div className="overflow-y-auto max-h-[85vh] p-6">
      {/* Close Button */}
      <button
        className="absolute top-2 right-4 text-2xl text-gray-600 hover:text-gray-800"
        onClick={() => {
          onClose();
        }}
      >
        ✖
      </button>

      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : recipe ? (
        <div>
          {/* Recipe Name */}
          <h1 className="text-3xl font-bold text-gray-800 text-center mb-6">
            {recipeName || "Unknown Recipe"}
          </h1>

           {/* Calories Display */}
        <p className="text-center text-xl text-gray-500 mb-4">
          Estimated Calories: {calories} kcal
        </p>

        <div className="w-full max-w-2xl mt-6 mb-4 flex space-x-4">
              {/* Collect Button */}
              <button
                className={`px-4 py-2 text-lg font-semibold rounded-lg ${
                  isCollected ? "bg-yellow-300 text-white-500" : "bg-gray-300 text-gray-500"
                }`}
                onClick={handleToggleCollection}
              >
                {isCollected ? "★ Collected" : "☆ Collect"}
              </button>

              {/* Cook Button */}
              <button
                className="px-4 py-2 text-lg font-semibold bg-green-500 text-white rounded-lg"
                onClick={handleCook}
              >
                🍳 Cook
              </button>
              <button
        onClick={getShoppingList}
        className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
      >
        🛒 Generate Shopping List
      </button>
            </div>


            <div className="my-4">
      {/* <button
        onClick={getShoppingList}
        className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
      >
        🛒 Generate Shopping List
      </button> */}

      {listLoading && <p className="text-gray-500 mt-2">Checking your fridge...</p>}

{error && <p className="text-red-500 mt-2">{error}</p>}

      {missingItems.length > 0 && (
        <div className="mt-4 border border-gray-300 p-4 rounded bg-yellow-50">
          <h2 className="font-semibold text-gray-800 mb-2">Items to Buy:</h2>
          <ul className="list-disc list-inside text-gray-700">
            {missingItems.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Ingredients Section */}
            <div className="border border-gray-300 rounded-lg p-4 bg-blue-50">
              <h2 className="text-xl font-semibold text-blue-900 mb-4">Ingredients</h2>
              <ul className="list-disc list-inside text-gray-600">
                {ingredient?.map((ingredient, index) => (
                  <li key={index}>{ingredient}</li>
                )) || <p>No ingredients listed.</p>}
              </ul>
            </div>

            {/* Steps Section */}
            <div className="md:col-span-2 border border-gray-300 rounded-lg p-4 bg-gray-50">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Steps</h2>
              <ol className="list-decimal list-inside text-gray-700">
                {recipe?.map((step, index) => (
                  <li key={index}> {step}</li>
                )) || <p>No steps provided.</p>}
              </ol>
            </div>
            
          </div>
        </div>
      ) : (
        <p>No recipe available.</p>
      )}
    </div>
    </div>
  </div>
);

}
