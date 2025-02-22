import React, {useState, useEffect} from "react";
import profilepic from "./assets/profilepic.png";
import recipepic from "./assets/recipepic.png";

const Profile = () => {
  const [tab, setTab] = useState("cooked");
  useEffect(() => {
    console.log('Active Tab:', tab);
  }, [tab]);
  const renderRightContent = () => {
    switch (tab) {
      case "preferences":
        return (
          <></>
        );
      case "collected":
      case "viewed":
      case "cooked":
        return (
          <>
            <h1 className="text-xl font-bold mb-4">Cooked Recipes</h1>
            <div className="space-y-4">
              {[1, 2, 3].map((item) => (
                <div
                  key={item}
                  className="flex items-center bg-gray-50 rounded-lg p-4 shadow-sm"
                >
                  {/* recipe pic */}
                  <img
                    className="w-20 h-20 rounded-lg"
                    src={recipepic}
                    alt="RecipePic"
                  />

                  {/* recipe info */}
                  <div className="ml-4 flex-1">
                    <div className="flex flex-row justify-between">
                      <h2 className="font-semibold text-lg">Recipe Name</h2>
                      <button className="text-gray-400 hover:text-gray-600">
                        ★
                      </button>
                    </div>
                    <div className="flex">
                      <p className="text-lg text-gray-500">Required Food:</p>
                    </div>
                    <div className="flex gap-2 mt-1">
                      {["Tomato", "Milk", "Onion"].map((food) => (
                        <span
                          key={food}
                          className="bg-black text-white px-2 py-1 text-xs rounded"
                        >
                          {food}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </>
          
        );
      default:
        return null;
      }
    }




  return (
    <div className="flex min-h-screen bg-gray-100 p-6">
      {/* left side */}
      <aside className="w-1/4 bg-white shadow-lg rounded-lg p-6">
        {/* profile pic */}
        <div className="flex flex-col items-center">
          <img
            className="w-24 h-24 rounded-full border-4 border-gray-300"
            src={profilepic}
            alt="ProfilePic"
          />
          <h2 className="mt-3 text-lg font-bold">Lily Chen</h2>
          <button onClick={()=>setTab("profile")} className="text-green-500 text-sm mt-1 hover:underline">
            Edit Profile
          </button>
        </div>

        {/* menu */}
        <nav className="flex flex-col mt-6 space-y-4">
          <button onClick={()=>setTab("preferences")} className="font-semibold text-gray-700">Preferences</button>
          <button onClick={()=>setTab("cooked")} className="font-semibold text-gray-700">Cooked Recipes</button>
          <button onClick={()=>setTab("viewed")} className="font-semibold text-gray-700">Viewed Recipes</button>
          <button onClick={()=>setTab("collected")} className="font-semibold text-gray-700">Collected Recipes</button>
          <button onClick={()=>setTab("profile")} className="font-semibold text-gray-700">User Profile</button>
        </nav>
      </aside>

      {/* content */}
      <main className="flex-1 ml-6 min-h-screen">
        <div className="bg-white shadow-lg rounded-lg p-6">
          {/* cooked recipes */}
          {renderRightContent()}

          {/* pagination */}
          <div className="mt-6 flex justify-between text-gray-500 text-sm">
            <button className="hover:text-black">← Previous</button>
            <div className="flex space-x-2">
              <button className="bg-black text-white px-3 py-1 rounded">
                1
              </button>
              <button className="hover:text-black">2</button>
              <button className="hover:text-black">3</button>
              <span>...</span>
              <button className="hover:text-black">67</button>
              <button className="hover:text-black">68</button>
            </div>
            <button className="hover:text-black">Next →</button>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Profile;
