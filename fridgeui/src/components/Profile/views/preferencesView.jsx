import React, { useEffect, useState, useContext } from "react";
import { LuX } from "react-icons/lu";
import api from "../../../api";
import { UserContext } from "./UserProvider";


const TagInput = ({ title, icon, tagList, onUpdate }) => {
  const [dynamicTags, setDynamicTags] = useState(tagList || []);
  const [inputValue, setInputValue] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [originalTags, setOriginalTags] = useState(tagList || []);
  

  useEffect(() => {
    setDynamicTags(tagList || []);
    setOriginalTags(tagList || []);
  }, [tagList]);

  const handleAddTag = () => {
    if (inputValue.trim() === "") return;
    const newTags = [...dynamicTags, inputValue.trim()];
    setDynamicTags(newTags);
    setInputValue("");
  };

  const handleRemoveTag = (tagToRemove) => {
    const newTags = dynamicTags.filter((tag) => tag !== tagToRemove);
    setDynamicTags(newTags);
  };

  const handleSave = () => {
    setIsEditing(false);
    onUpdate(dynamicTags);
  };

  const handleCancel = () => {
    setIsEditing(false);
    setDynamicTags(originalTags);
  };

  return (
    
    <div className="bg-white rounded-2xl shadow-md p-4 mb-6">
      <div className="flex items-center gap-2 mb-3">
        {icon}
        <h2 className="font-semibold text-lg">{title}</h2>
      </div>
      <div className="flex flex-col gap-2">
        <div className="flex flex-wrap gap-1">
          {dynamicTags.map((tag, idx) => (
            <div
              key={idx}
              className="flex bg-black text-white px-2 py-1 text-xs rounded-lg"
            >
              <span>{tag}</span>
              {isEditing && (
                <button onClick={() => handleRemoveTag(tag)} className="ml-1">
                  <LuX />
                </button>
              )}
            </div>
          ))}
        </div>
        {isEditing && (
          <div className="flex justify-end">
            <input
              type="text"
              placeholder="add your tag :)"
              onChange={(e) => setInputValue(e.target.value)}
              value={inputValue}
              onKeyUp={(e) => {
                if (e.key === "Enter") {
                  handleAddTag();
                }
              }}
              className="border rounded-full px-4 py-1 text-sm outline-none"
            />
            {/* <button
              onClick={handleAddTag}
              className="ml-2 bg-blue-500 text-white px-3 py-1 rounded-md text-sm"
            >
              Add
            </button> */}
          </div>
        )}
      </div>
      {/* Edit & Save Buttons */}
      <div className="flex justify-end mt-4 space-x-2">
        {isEditing ? (
          <>
            <button
              onClick={handleSave}
              className="bg-green-500 text-white px-3 py-1 rounded-md text-sm"
            >
              Save
            </button>
            <button
              onClick={handleCancel}
              className="bg-gray-400 text-white px-3 py-1 rounded-md text-sm"
            >
              Cancel
            </button>
          </>
        ) : (
          <button
            onClick={() => setIsEditing(true)}
            className="bg-gray-700 text-white px-3 py-1 rounded-md text-sm"
          >
            Edit
          </button>
        )}
      </div>
    </div>
  );
};

const PreferencesView = () => {
  const { userinfo, setUserinfo } = useContext(UserContext);
  const [recommendation, setRecommendation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  //   const [likes, setLikes] = useState([]);
  //   const [dislikes, setDislikes] = useState([]);
  //   const [allergies, setAllergies] = useState([]);

  const updateUserTags = async (field, newTags) => {
    try {
      const updatedUser = { ...userinfo, [field]: newTags.join(",") };
      const patchData = { [field]: newTags.join(",") };
      const response = await api.patch(
        `/core/users/${userinfo.id}/`,
        patchData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },}
    );
      if (response.status !== 200)
        throw new Error("Failed to update user data");

      setUserinfo(updatedUser);
    //   console.log(`Updated ${field}:`, newTags);
    } catch (error) {
      console.error(`Error updating ${field}:`, error);
    }
  };

  const getDailyRecommendation = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await api.get("/core/users/daily_recommand/", {
        params: { userid: userinfo.id },
      });
      if (response.status === 200 && response.data.success) {
        setRecommendation(response.data.data);
      } else {
        setError("Failed to fetch daily recommendation.");
      }
    } catch (err) {
      setError("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Main Content */}

      <TagInput
        title="What I like?"
        icon={<span className="text-xl">💜</span>}
        tagList={userinfo?.userlike ? userinfo.userlike.split(",") : []}
        onUpdate={(newTags) => updateUserTags("userlike", newTags)}
      />
      <TagInput
        title="What I dislike?"
        icon={<span className="text-xl">❌</span>}
        tagList={userinfo?.dislike ? userinfo.dislike.split(",") : []}
        onUpdate={(newTags) => updateUserTags("dislike", newTags)}
      />
      <TagInput
        title="Allergies"
        icon={<span className="text-xl">❗</span>}
        tagList={userinfo?.allergies ? userinfo.allergies.split(",") : []}
        onUpdate={(newTags) => updateUserTags("allergies", newTags)}
      />

<div className="text-center mt-4">
        <button
          onClick={getDailyRecommendation}
          className="bg-gradient-to-l from-green-400 to-green-600 hover:from-green-700 hover:to-green-500 text-white px-5 py-2 rounded-lg shadow"
        >
          🍽 Get Daily Recommendation
        </button>

        {loading && <p className="mt-2 text-gray-500">Loading...</p>}
        {error && <p className="text-red-500 mt-2">{error}</p>}

        {recommendation && (
          <div className="mt-6 text-left border p-4 rounded-md bg-yellow-50">
            {Object.entries(recommendation).map(([meal, detail]) => (
              <div key={meal} className="mb-4">
                <h3 className="text-lg font-semibold capitalize">🍴 {meal}</h3>
                <p><strong>Recipe:</strong> {detail.recipename}</p>
                <p><strong>Calories:</strong> {detail.calories}</p>
                <p><strong>Flavors:</strong> {detail.flavor_tags.join(", ")}</p>
                <p><strong>Ingredients:</strong> {detail.ingredients.join(", ")}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
};

export default PreferencesView;
