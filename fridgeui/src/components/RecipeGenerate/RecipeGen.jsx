import { useState, useEffect, useContext } from 'react';
import api from '../../api';
import potpic from "./assets/potpic.png";
import React from 'react';
import Navbar from "../../components/Navbar";
import RecipeDetail from "../RecipeDetail/RecipeDetail";
import { UserContext } from "../Profile/views/UserProvider";

const FridgeRecipePage = ({ userId, recipeId }) => {
  const [foods, setFoods] = useState([]);
  const [tags, setTags] = useState([]);
  const [initialFoods, setInitialFoods] = useState([]);
  const [initialTags, setInitialTags] = useState([]);
  const [droppedItems, setDroppedItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [flavorQuery, setFlavorQuery] = useState('');
  const [isCooking, setIsCooking] = useState(false);
  const [isFalling, setIsFalling] = useState(false);
  const [isRecipeLoading, setIsRecipeLoading] = useState(false);
  const [showRecipeButtons, setShowRecipeButtons] = useState(false);
  const [selectedRecipeId, setSelectedRecipeId] = useState(null);
  const { userinfo } = useContext(UserContext);

  const [topRecipes, setTopRecipes] = useState([]);

  useEffect(() => {
    async function fetchRecipe() {
      try {
        const response = await api.get(`core/fridge/search_food_list/`);
        const data = response.data.data;
        if (data && data.foods && data.tags) {
          setFoods(data.foods);
          setTags(data.tags);
          setInitialFoods(data.foods);
          setInitialTags(data.tags);
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

  const handleSearch = async () => {
    try {
      const trimmedQuery = searchQuery.trim();
      const url = trimmedQuery === ""
        ? `core/fridge/search_food_list/`
        : `core/fridge/search_food_list/?name=${trimmedQuery}`;
      const response = await api.get(url);
      const data = response.data.data;
      if (data && data.foods) {
        setFoods(data.foods);
      } else {
        setFoods([]);
      }
    } catch (err) {
      setError("Failed to fetch food.");
    }
  };

  const handleFlavorKeyDown = (e) => {
    if (e.key === 'Enter') {
      const trimmedFlavor = flavorQuery.trim();
      if (trimmedFlavor && !tags.includes(trimmedFlavor)) {
        setTags(prev => [...prev, trimmedFlavor]);
      }
      setFlavorQuery('');
    }
  };

  const handleDragStart = (e, item, source) => {
    e.dataTransfer.setData("text/plain", item);
    e.dataTransfer.setData("source", source);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  // Drop into the pot
  const handleDrop = (e) => {
    e.preventDefault();
    const item = e.dataTransfer.getData("text/plain");
    const source = e.dataTransfer.getData("source");

    const currentCount = droppedItems.filter(d => d.type === source).length;
    if (source === "food" && currentCount >= 3) {
      alert("You can only add up to 3 food items.");
      return;
    }
    if (source === "flavor" && currentCount >= 2) {
      alert("You can only add up to 2 flavor items.");
      return;
    }

    const newDroppedItem = { item, type: source };
    setDroppedItems(prev => [...prev, newDroppedItem]);

    if (source === "food") {
      setFoods(prevFoods => prevFoods.filter(f => f.name !== item));
    } else if (source === "flavor") {
      setTags(prevTags => prevTags.filter(t => t !== item));
    }
  };

  const handleReturnToFood = (e) => {
    e.preventDefault();
    const item = e.dataTransfer.getData("text/plain");
    const source = e.dataTransfer.getData("source");

    if (source === "food") {
      setDroppedItems(prev => prev.filter(d => d.item !== item));
      const foodObj = initialFoods.find(f => f.name === item);
      if (foodObj) {
        setFoods(prev => [...prev, foodObj]);
      }
    }
  };

  const handleReturnToFlavor = (e) => {
    e.preventDefault();
    const item = e.dataTransfer.getData("text/plain");
    const source = e.dataTransfer.getData("source");

    if (source === "flavor") {
      setDroppedItems(prev => prev.filter(d => d.item !== item));
      setTags(prev => [...prev, item]);
    }
  };

  // Primary "Cook or Restore" button
  const handleCookOrRestore = async () => {
    if (showRecipeButtons) {
      // RESTORE
      setFoods(initialFoods);
      setTags(initialTags);
      setDroppedItems([]);
      setShowRecipeButtons(false);
      setIsRecipeLoading(false);
      setSearchQuery('');
      setTopRecipes([]);
    } else {

      const ingredientNames = droppedItems.map(d => d.item);


      try {
        const queryString = encodeURIComponent(ingredientNames.join(", "));
        const response = await api.get(
          `core/fridge/get_recipe/?ingredient=${queryString}`
        );
        const recipes = response?.data?.data?.recipes || [];

        setTopRecipes(recipes.slice(0, 2));
      } catch (err) {
        console.error("Failed to get recipe:", err);
        setTopRecipes([]);
      }

      setIsFalling(true);
      setIsCooking(true);
      setTimeout(() => {
        setDroppedItems([]);
        setIsFalling(false);
      }, 1000);

      setTimeout(() => {
        setIsCooking(false);
        setIsRecipeLoading(true);
      }, 2000);

      setTimeout(() => {
        setIsRecipeLoading(false);
        setShowRecipeButtons(true);
      }, 4000);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!foods.length && !tags.length) return <p>No items available.</p>;

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      <style>{`
        @keyframes shake {
          0% { transform: translateX(0); }
          25% { transform: translateX(-10px); }
          50% { transform: translateX(10px); }
          75% { transform: translateX(-10px); }
          100% { transform: translateX(0); }
        }
        .shake-animation {
          animation: shake 0.5s ease-in-out 4;
        }
        @keyframes popOut {
          0% { transform: translateY(0); opacity: 0; }
          50% { opacity: 1; }
          100% { transform: translateY(-100px); opacity: 1; }
        }
        .pop-out-animation {
          animation: popOut 1s ease forwards;
        }
      `}</style>

      <Navbar />

      <main className="flex flex-1 gap-4 p-4">
        <section className="flex-1 bg-white rounded-lg shadow p-4">
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') handleSearch(); }}
              placeholder="Search your items..."
              className="border rounded-full py-2 pl-4 pr-10 w-full"
            />
            <button
              onClick={handleSearch}
              className="absolute right-2 top-2 text-gray-500"
            >
              🔍
            </button>
          </div>
          <div
            className="mt-4 space-y-2 overflow-y-auto max-h-96"
            onDrop={handleReturnToFood}
          >
            {foods.map((food, index) => {
              const now = new Date();
              const expireDate = new Date(food.expire_time);
              const oneDayLater = new Date(now.getTime() + 24 * 60 * 60 * 1000);
              const isExpiringSoon = expireDate <= oneDayLater;

              return (
                <div
                  key={index}
                  className="border rounded-lg flex items-center p-2 h-16 cursor-move"
                  draggable
                  onDragStart={(e) => handleDragStart(e, food.name, 'food')}
                >
                  <div className="flex flex-col">
                    <span className="font-semibold">{food.name}</span>
                    <span className={isExpiringSoon ? "text-red-500 text-sm" : "text-gray-500 text-sm"}>
                      Exp: {food.expire_time}
                    </span>
                  </div>
                  <img
                    src={food.pic || "foodPicPlaceholder"}
                    alt={food.name}
                    className="ml-auto h-10"
                  />
                </div>

              );
            })}

          </div>
        </section>

        <section
          className="flex-1 bg-white rounded-lg shadow p-4 relative flex flex-col items-center justify-center"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          <div
            className="absolute left-1/2 transform -translate-x-1/2 flex flex-col items-center space-y-2"
            style={{
              top: isFalling ? "50%" : "2rem",
              opacity: isFalling ? 0 : 1,
              transition: "top 1s ease, opacity 1s ease"
            }}
          >
            {droppedItems.map((d, idx) => (
              <div
                key={idx}
                className="bg-yellow-100 border border-yellow-400 rounded px-3 py-1"
              >
                {d.item}
              </div>
            ))}
          </div>

          <button
            onClick={handleCookOrRestore}
            style={{ backgroundColor: 'white' }}
            className="absolute z-10 top-[50%] left-1/2 transform -translate-x-1/2 px-4 py-2 text-black text-xl rounded"
          >
            {showRecipeButtons ? "restore" : "start cook"}
          </button>

          <img
            src={potpic}
            alt="pot"
            className={`mt-4 ${isCooking ? 'shake-animation' : ''}`}
          />

          {showRecipeButtons && (
            <>
              {topRecipes[0] && (
                <button
                  className="pop-out-animation"
                  style={{
                    position: 'absolute',
                    top: '20%',
                    left: '25%',
                    width: '110px',
                    height: '110px',
                    borderRadius: '50%',
                    backgroundColor: 'white',
                    border: '2px solid #ccc',
                    fontSize: '0.9rem',
                    color: 'black',
                    overflow: 'hidden',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    textAlign: 'center',
                    padding: '6px'
                  }}
                  onClick={() => setSelectedRecipeId(topRecipes[0].id)}

                >
                  {/* Show recipe name (or ID) */}
                  {topRecipes[0].name}
                </button>
              )}

              {topRecipes[1] && (
                <button
                  className="pop-out-animation"
                  style={{
                    position: 'absolute',
                    top: '20%',
                    right: '25%',
                    width: '110px',
                    height: '110px',
                    borderRadius: '50%',
                    backgroundColor: 'white',
                    border: '2px solid #ccc',
                    fontSize: '0.9rem',
                    color: 'black',
                    overflow: 'hidden',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    textAlign: 'center',
                    padding: '6px'
                  }}
                  onClick={() => setSelectedRecipeId(topRecipes[1].id)}

                >
                  {topRecipes[1].name}
                </button>
              )}
            </>
          )}

          {isRecipeLoading && (
            <div
              className="absolute z-20 flex items-center justify-center"
              style={{
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)"
              }}
            >
              <div className="w-12 h-12 border-4 border-gray-500 border-dashed rounded-full animate-spin"></div>
            </div>
          )}
        </section>

        <section className="flex-1 bg-white rounded-lg shadow p-4">
          <input
            type="text"
            value={flavorQuery}
            onChange={(e) => setFlavorQuery(e.target.value)}
            onKeyDown={handleFlavorKeyDown}
            placeholder="Search flavor..."
            className="border rounded-full py-2 pl-4 w-full"
          />
          <div
            className="mt-4 flex flex-col gap-2 overflow-y-auto max-h-96"
            onDrop={handleReturnToFlavor}
          >
            {tags.map((tag, index) => (
              <div
                key={tag}
                draggable
                onDragStart={(e) => handleDragStart(e, tag, "flavor")}
                className="inline-block bg-gray-800 text-white rounded px-2 py-1 cursor-move"
              >
                {tag}
              </div>
            ))}
          </div>
        </section>
      </main>
      {selectedRecipeId && (
        <RecipeDetail
          userId={userinfo.id}
          recipeId={selectedRecipeId}
          onClose={() => setSelectedRecipeId(null)}
        />
      )}
    </div>


  );
};

export default FridgeRecipePage;
