import React from 'react'
import recipepic from "../assets/recipepic.png";

const cookedView = () => {
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
  )
}

export default cookedView