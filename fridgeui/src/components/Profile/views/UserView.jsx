import React, { useContext, useEffect, useState } from "react";
import { UserContext } from "./UserProvider";
import api from "../../../api";

const UserView = () => {
  const { userinfo, setUserinfo, loading, error } = useContext(UserContext);
  const [isEditing, setIsEditing] = useState(false);
  const [tempUser, setTempUser] = useState({});

  useEffect(() => {
    setTempUser(userinfo);
  }, [userinfo]);

  const calculateBMI = (height, weight) => {
    if (!height || !weight) return "";
    const bmi = weight / (height * height);
    return bmi.toFixed(2);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    const updatedUser = { ...tempUser, [name]: value };
    if (name === "height" || name === "weight") {
      updatedUser.BMI = calculateBMI(updatedUser.height, updatedUser.weight);
    }
    setTempUser(updatedUser);
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setUserinfo({ ...tempUser, profilePicture: URL.createObjectURL(file) });
    }
  };

  const handleSave = async () => {
    try {
      // Send a PATCH request to update the user info
      const response = await api.patch(`/core/users/${tempUser.id}/`, tempUser);
      if (response.status !== 200) {
        throw new Error("Failed to update user info");
      }
      alert("User info updated successfully!");
      setUserinfo(tempUser);
    } catch (err) {
      console.error(err);
      alert("Failed to update user info");
    } finally {
      setIsEditing(false);
    }
  };
  //   useEffect(() => {
  //     console.log('loading', loading);
  //     console.log('error', error);
  //   }, [loading, error]);

  return loading ? (
    <p>Loading...</p>
  ) : error ? (
    <p className="text-red-500">Error: {error}</p>
  ) : (
    <>
      {/* Profile Form */}
      <form className="space-y-4">
        {/* Username */}
        <div>
          <label className="block text-gray-600">Username</label>
          <input
            type="text"
            name="username"
            value={tempUser?.username || ""}
            onChange={handleInputChange}
            disabled={!isEditing}
            className="w-full p-2 border rounded-md"
          />
        </div>

        {/* Gender
          <div>
            <label className="block text-gray-600">Gender</label>
            <input
              type="text"
              name="gender"
              value={tempUser?.gender ||""}
              onChange={handleInputChange}
              disabled={!isEditing}
              className="w-full p-2 border rounded-md"
            />
          </div> */}

        {/* Weight */}
        <div>
          <label className="block text-gray-600">Weight(kg)</label>
          <input
            type="text"
            name="weight"
            value={tempUser?.weight || ""}
            onChange={handleInputChange}
            disabled={!isEditing}
            className="w-full p-2 border rounded-md"
          />
        </div>

        {/* Height */}
        <div>
          <label className="block text-gray-600">Height(m)</label>
          <input
            type="text"
            name="height"
            value={tempUser?.height || ""}
            onChange={handleInputChange}
            disabled={!isEditing}
            className="w-full p-2 border rounded-md"
          />
        </div>

        {/* BMI */}
        <div>
          <label className="block text-gray-600">BMI</label>
          <input
            type="text"
            name="BMI"
            value={tempUser?.BMI || ""}
            disabled={true}
            className="w-full p-2 border rounded-md"
          />
        </div>

        {/* note */}
        <div className="bg-blue-100 border-l-4 border-blue-500 text-blue-700 p-4 rounded-lg shadow-md mt-4">
          <h3 className="font-bold text-lg">📌 BMI Health Note</h3>
          <p className="mt-2">
            ✅ <span className="font-semibold">Healthy BMI</span> is between{" "}
            <span className="text-green-600 font-semibold">18.5 - 24.9</span>.
          </p>
          <p className="mt-1">
            ❗{" "}
            <span className="font-semibold text-red-500">
              BMI does not account
            </span>{" "}
            for{" "}
            <span className="italic">
              muscle mass, bone density, or body composition
            </span>
            .
          </p>
          <p>🔗{" "}<a className="underline italic" target="_blank" rel="noopener noreferrer" href="https://www.canada.ca/en/health-canada/services/food-nutrition/healthy-eating/healthy-weights/canadian-guidelines-body-weight-classification-adults/questions-answers-public.html#a2">reference</a></p>
        </div>

        {/* Profile Picture Upload */}
        <div>
          <label className="block text-gray-600">Profile Picture</label>
          <div className="border p-4 flex flex-col items-center">
            {tempUser?.profilePicture ? (
              <img
                src={tempUser.profilePicture}
                alt="Uploaded"
                className="w-24 h-24 rounded-md mb-2"
              />
            ) : (
              <div className="w-24 h-24 bg-gray-200 rounded-md flex items-center justify-center">
                <span className="text-gray-500">No Image</span>
              </div>
            )}
            {isEditing && (
              <input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="mt-2"
              />
            )}
          </div>
        </div>

        {/* Buttons */}
        <div className="flex justify-between">
          {isEditing ? (
            <button
              type="button"
              onClick={() => handleSave()}
              className="bg-green-500 text-white px-4 py-2 rounded"
            >
              Save
            </button>
          ) : (
            <button
              type="button"
              onClick={() => setIsEditing(true)}
              className="bg-gray-700 text-white px-4 py-2 rounded"
            >
              Edit
            </button>
          )}
        </div>
      </form>
    </>
  );
};

export default UserView;
