import React, { useState, useEffect } from "react";
import { fetchFridgeItems, addFridgeItem, deleteFridgeItem, fetchFoodTags } from "../../api";
import Navbar from "../../components/Navbar";

const FridgePage = () => {
  const [fridgeItems, setFridgeItems] = useState([]);
  const [expiringItems, setExpiringItems] = useState([]);
  const [foodTags, setFoodTags] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searchTerm, setSearchTerm] = useState("");

  const getCurrentDate = () => new Date().toISOString().split("T")[0];

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newFood, setNewFood] = useState({
    name: "",
    user_id: "",
    add_time: getCurrentDate(),
    expire_time: "",
    tag: "", 
  });


  const [sortBy, setSortBy] = useState("create_time_desc"); // Default sort option
  useEffect(() => {
    loadItems();
    loadFoodTags();
  }, [searchTerm, sortBy]);
  const loadItems = async () => {
    setLoading(true);
    try {
      const items = await fetchFridgeItems(1, 20, sortBy, searchTerm); // Include sortBy in API call
      const now = new Date();
      const expiring = items.filter(
        (item) => new Date(item.expire_time) <= new Date(now.getTime() + 3 * 24 * 60 * 60 * 1000)
      );
      setExpiringItems(expiring);
      setFridgeItems(items.filter((item) => !expiring.includes(item)));
    } catch (err) {
      setError("Failed to load items.");
    } finally {
      setLoading(false);
    }
  };
  

  
  const loadFoodTags = async () => {
    try {
      const tags = await fetchFoodTags();
      setFoodTags(tags);
    } catch (err) {
      console.error("Failed to fetch food tags.");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this item?")) return;
    const result = await deleteFridgeItem(id);
    if (result?.success) {
      loadItems();
    } else {
      alert("Failed to delete item.");
    }
  };

  const handleAddFood = async () => {
    if (!newFood.name  || !newFood.add_time || !newFood.expire_time || !newFood.tag) {
      alert("Please fill in all fields.");
      return;
    }

    const result = await addFridgeItem(newFood);
    if (result) {
      setIsModalOpen(false);
      setNewFood({ name: "", user_id: "", add_time: getCurrentDate(), expire_time: "", tag: "" });
      loadItems();
    } else {
      alert("Failed to add food.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 font-sans">
      <Navbar /> {/* Add Navbar here */}
      <main className="p-8">
        <section className="flex gap-4">
          {/* Expiring Items */}
{/* Expiring Items */}
<div className="bg-white p-4 shadow rounded-lg w-60">
  <h3 className="font-semibold text-red-500">Expiring Soon</h3>
  <ul className="mt-4 space-y-3 overflow-y-auto max-h-60">
    {expiringItems.map((item) => (
      <li key={item.id} className="flex items-center gap-2 border-b pb-2 relative">
        <button
          onClick={() => handleDelete(item.id)}
          className="absolute top-1 right-1 text-xs bg-red-500 text-white px-2 py-1 rounded"
        >
          ✕
        </button>
        <img src={item.icon || "https://placehold.co/50x50/png"} alt={item.name} className="h-8 w-8" />
        <span className="text-red-500">{item.name}</span>
      </li>
    ))}
  </ul>
</div>

          {/* Fridge Items */}
 {/* Fridge Items (修正 grid 结构) */}
<div className="bg-white p-4 shadow rounded-lg flex-grow">
  <div className="flex items-center gap-2 mb-4">
    <input
      className="border rounded-lg px-2 py-1 flex-grow"
      placeholder="Search ingredients"
      value={searchTerm}
      onChange={(e) => setSearchTerm(e.target.value)}
    />
     {/* Sorting Dropdown */}
  <select
    className="border rounded-lg px-2 py-1"
    value={sortBy}
    onChange={(e) => setSortBy(e.target.value)}
  >
    <option value="create_time_desc">Newest</option>
    <option value="create_time">Oldest</option>
    <option value="tag">Category</option>
  </select>
  </div>

  <div className="border rounded-lg p-4 bg-gray-100">
    {loading ? (
      <p>Loading...</p>
    ) : error ? (
      <p className="text-red-500">{error}</p>
    ) : (
      <div className="grid grid-cols-5 gap-2">
        {fridgeItems
          .filter((item) => item.name.toLowerCase().includes(searchTerm.toLowerCase()))
          .map((item) => (
            <div key={item.id} className="bg-white flex flex-col items-center p-2 shadow rounded-lg relative">
              <button
                onClick={() => handleDelete(item.id)}
                className="absolute top-1 right-1 text-xs bg-red-500 text-white px-2 py-1 rounded"
              >
                ✕
              </button>
              <img src={item.icon || "https://placehold.co/50x50/png"} alt={item.name} className="h-8 w-8" />
              <span>{item.name}</span>
            </div>
          ))}
      </div>
    )}
  </div>
</div>
        </section>
      </main>

      {/* Add Food Button */}
      <button
        onClick={() => setIsModalOpen(true)}
        className="fixed bottom-6 right-6 bg-blue-500 text-white px-4 py-2 rounded-full shadow-lg"
      >
        + Add Food
      </button>

      {/* Add Food Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96">
            <h2 className="text-xl font-semibold mb-4">Add Food</h2>
            <input
              type="text"
              placeholder="Food Name"
              value={newFood.name}
              onChange={(e) => setNewFood({ ...newFood, name: e.target.value })}
              className="border px-3 py-2 w-full mb-2"
            />
            
            {/* Tag Selection Dropdown */}
            <div className="mb-4">
              <label className="block text-gray-700">Category:</label>
              <select
                value={newFood.tag}
                onChange={(e) => setNewFood({ ...newFood, tag: e.target.value })}
                className="border px-3 py-2 w-full"
              >
                <option value="">Select Category</option>
                {Object.entries(foodTags).map(([tag, info]) => (
                  <option key={tag} value={tag}>
                    {info.name}
                  </option>
                ))}
              </select>
              {newFood.tag && foodTags[newFood.tag] && (
                <img src={foodTags[newFood.tag].icon} alt="Tag Icon" className="h-8 w-8 mt-2" />
              )}
            </div>
     {/* Add Time Input */}
     <div className="flex items-center mb-4">
        <span className="w-24 text-gray-700">Add Time:</span>
        <input
          type="date"
          value={newFood.add_time}
          onChange={(e) => setNewFood({ ...newFood, add_time: e.target.value })}
          className="border px-3 py-2 w-full"
        />
      </div>

      {/* Expire Time Input */}
      <div className="flex items-center mb-4">
        <span className="w-24 text-gray-700">Expire Time:</span>
        <input
          type="date"
          value={newFood.expire_time}
          onChange={(e) => setNewFood({ ...newFood, expire_time: e.target.value })}
          className="border px-3 py-2 w-full"
        />
      </div>
            <div className="flex justify-end gap-2">
              <button onClick={() => setIsModalOpen(false)} className="px-4 py-2 bg-gray-300 rounded">Cancel</button>
              <button onClick={handleAddFood} className="px-4 py-2 bg-blue-500 text-white rounded">Add</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FridgePage;
