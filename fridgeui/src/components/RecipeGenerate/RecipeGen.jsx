import { useState, useEffect } from 'react';
import api from '../../api'; 
import potpic from "./assets/potpic.png";  
import React from 'react';
import Navbar from "../../components/Navbar";

const FridgeRecipePage = ({ userId, recipeId }) => {
  const [foods, setFoods] = useState([]);
  const [tags, setTags] = useState([]);
  const [initialFoods, setInitialFoods] = useState([]); // Save initial foods data
  const [initialTags, setInitialTags] = useState([]);   // Save initial tags data
  // Stores dropped items; each item is an object { item, type }
  const [droppedItems, setDroppedItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState(''); // Input for searching food
  const [flavorQuery, setFlavorQuery] = useState(''); // Input for searching flavor
  const [isCooking, setIsCooking] = useState(false); // Whether the pot is shaking (cooking)
  const [isFalling, setIsFalling] = useState(false);   // Controls falling animation for items
  const [isRecipeLoading, setIsRecipeLoading] = useState(false); // Controls recipe loading animation
  const [showRecipeButtons, setShowRecipeButtons] = useState(false); // Controls display of recipe buttons

  // Use recipeId as the recipe name for now; adjust as needed
  const recipeName = recipeId || "Recipe";

  useEffect(() => {
    async function fetchRecipe() {
      try {
        const userId = 111;
        const response = await api.get(`core/get_food_list/?uid=${userId}`);
        const data = response.data.data; // Get the data from response
        console.log(data.foods);
        // Check if the response contains foods and tags
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

  // Function to handle food search:
  // If searchQuery is empty, return all data; otherwise, call the search API.
  const handleSearch = async () => {
    try {
      const userId = 111;
      const trimmedQuery = searchQuery.trim();
      const url = trimmedQuery === ""
        ? `core/get_food_list/?uid=${userId}`
        : `core/get_food_list/?uid=${userId}&query=${trimmedQuery}`;
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

  // Right-side flavor search:
  // On Enter key, if the input flavor does not exist in tags, add it.
  const handleFlavorKeyDown = (e) => {
    if (e.key === 'Enter') {
      const trimmedFlavor = flavorQuery.trim();
      if (trimmedFlavor && !tags.includes(trimmedFlavor)) {
        setTags(prev => [...prev, trimmedFlavor]);
      }
      setFlavorQuery('');
    }
  };

  // On drag start, store the item and its source in dataTransfer.
  const handleDragStart = (e, item, source) => {
    e.dataTransfer.setData("text/plain", item);
    e.dataTransfer.setData("source", source);
  };

  // Prevent default when dragging over a drop target.
  const handleDragOver = (e) => {
    e.preventDefault();
  };

  // When an item is dropped onto the pot area, add it to droppedItems
  // and remove it from the corresponding list; enforce limits.
  const handleDrop = (e) => {
    e.preventDefault();
    const item = e.dataTransfer.getData("text/plain");
    const source = e.dataTransfer.getData("source");

    // Count current dropped items of the same type.
    const currentCount = droppedItems.filter(d => d.type === source).length;
    if (source === "food" && currentCount >= 3) {
      alert("You can only add up to 3 food items.");
      return; // Exceeds limit, do not update state.
    }
    if (source === "flavor" && currentCount >= 2) {
      alert("You can only add up to 2 flavor items.");
      return; // Exceeds limit, do not update state.
    }

    // Within limit: add the new dropped item.
    const newDroppedItem = { item, type: source };
    setDroppedItems(prev => [...prev, newDroppedItem]);

    if (source === "food") {
      setFoods(prevFoods => prevFoods.filter(f => f !== item));
    } else if (source === "flavor") {
      setTags(prevTags => prevTags.filter(t => t !== item));
    }
  };

  // Allow items to be dragged back to the food list (left side)
  const handleReturnToFood = (e) => {
    e.preventDefault();
    const item = e.dataTransfer.getData("text/plain");
    const source = e.dataTransfer.getData("source");
    if (source === "food") {
      setDroppedItems(prev => prev.filter(d => d.item !== item));
      setFoods(prev => [...prev, item]);
    }
  };

  // Allow items to be dragged back to the flavor list (right side)
  const handleReturnToFlavor = (e) => {
    e.preventDefault();
    const item = e.dataTransfer.getData("text/plain");
    const source = e.dataTransfer.getData("source");
    if (source === "flavor") {
      setDroppedItems(prev => prev.filter(d => d.item !== item));
      setTags(prev => [...prev, item]);
    }
  };

  // Handle the button click:
  // If recipe buttons are showing ("restore" state), restore initial state.
  // Otherwise, execute the "start cook" process.
  const handleCookOrRestore = () => {
    if (showRecipeButtons) {
      // Restore: revert to the initial state.
      setFoods(initialFoods);
      setTags(initialTags);
      setDroppedItems([]);
      setShowRecipeButtons(false);
      setIsRecipeLoading(false);
      setSearchQuery('');
    } else {
      // Execute start cook process.
      setIsFalling(true);
      setIsCooking(true);
      setTimeout(() => {
        setDroppedItems([]);
        setIsFalling(false);
      }, 1000);
      setTimeout(() => {
        setIsCooking(false);
        // Start loading animation for 2 seconds.
        setIsRecipeLoading(true);
      }, 2000);
      setTimeout(() => {
        setIsRecipeLoading(false);
        setShowRecipeButtons(true);
      }, 4000); // 2000ms + 2000ms = 4000ms, then show recipe buttons.
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>{error}</p>;
  if (!foods.length && !tags.length) return <p>No items available.</p>;

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col">
      {/* Internal styles: pot shake animation and recipe buttons pop-out animation */}
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

      {/* Header */}
      <Navbar />

      {/* Main content */}
      <main className="flex flex-1 gap-4 p-4">
        {/* Left side: Food */}
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
          {/* Food list container becomes a drop zone for food items */}
          <div 
            className="mt-4 space-y-2 overflow-y-auto max-h-96"
            onDragOver={handleDragOver}
            onDrop={handleReturnToFood}
          >
            {foods.map((food, index) => (
              <div
                key={index}
                className="border rounded-lg flex items-center p-2 h-12 cursor-move"
                draggable
                onDragStart={(e) => handleDragStart(e, food, "food")}
              >
                <span className="font-semibold">{food}</span>
                <img
                  src="foodPicPlaceholder"
                  alt={food}
                  className="ml-auto h-10"
                />
              </div>
            ))}
          </div>
        </section>

        {/* Center: Pot (drop zone) */}
        <section
          className="flex-1 bg-white rounded-lg shadow p-4 relative flex flex-col items-center justify-center"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
        >
          {/* Display dropped items with falling animation */}
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

          {/* Center button: shows "start cook" or "restore" depending on state */}
          <button
            onClick={handleCookOrRestore}
            style={{ backgroundColor: 'white' }}
            className="absolute z-10 top-[50%] left-1/2 transform -translate-x-1/2 px-4 py-2 text-black text-xl rounded"
          >
            {showRecipeButtons ? "restore" : "start cook"}
          </button>

          {/* Pot image with shake animation if isCooking is true */}
          <img
            src={potpic}
            alt="pot"
            className={`mt-4 ${isCooking ? 'shake-animation' : ''}`}
          />

          {/* When recipe buttons are shown, display two circular buttons (110px × 110px) at 20% from the top */}
          {showRecipeButtons && (
            <>
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
                  fontSize: '1rem',
                  color: 'black'
                }}
              >
                {recipeName}
              </button>
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
                  fontSize: '1rem',
                  color: 'black'
                }}
              >
                {recipeName}
              </button>
            </>
          )}

          {/* Display loading spinner when recipe is loading (spinner in gray) */}
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

        {/* Right side: Flavor */}
        <section className="flex-1 bg-white rounded-lg shadow p-4">
          <input
            type="text"
            value={flavorQuery}
            onChange={(e) => setFlavorQuery(e.target.value)}
            onKeyDown={handleFlavorKeyDown}
            placeholder="Search flavor..."
            className="border rounded-full py-2 pl-4 w-full"
          />
          {/* Flavor list container becomes a drop zone for flavor items */}
          <div 
            className="mt-4 flex flex-col gap-2 overflow-y-auto max-h-96"
            onDragOver={handleDragOver}
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
    </div>
  );
};

export default FridgeRecipePage;
