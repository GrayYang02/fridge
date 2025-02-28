import React from "react";

const RecipePage = () => {
  return (
    <div className="min-h-screen bg-gray-100 flex justify-center py-10">
      <div className="bg-white shadow-lg rounded-lg p-6 max-w-4xl w-full">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-6">
          Apple Pie Recipe
        </h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Ingredients Section */}
          <div className="border border-gray-300 rounded-lg p-4 bg-blue-50">
            <h2 className="text-xl font-semibold text-blue-900 mb-4">Ingredients</h2>
            
            <h3 className="text-md font-semibold text-gray-700">For the Pie:</h3>
            <ul className="list-disc list-inside text-gray-600 mb-4">
              <li>1 unbaked pie crust</li>
              <li>3 large (or 4-5 small) Granny Smith apples, peeled, cored, and sliced thin</li>
              <li>1/2 cup brown sugar</li>
              <li>1/2 cup sugar</li>
              <li>1 Tbsp. all-purpose flour</li>
              <li>1/2 cup heavy cream</li>
              <li>2 tsp. vanilla extract</li>
              <li>1/8 tsp. cinnamon</li>
              <li>Ice cream, whipped cream, or <a href="#" className="text-blue-600 underline">hard sauce</a>, for serving</li>
            </ul>

            <h3 className="text-md font-semibold text-gray-700">For the Topping:</h3>
            <ul className="list-disc list-inside text-gray-600">
              <li>7 Tbsp. butter</li>
              <li>3/4 cup all-purpose flour</li>
              <li>1/2 cup brown sugar</li>
              <li>1/4 cup pecans (more to taste)</li>
              <li>Dash of salt</li>
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
                <button className="bg-gray-700 text-white px-4 py-2 rounded-lg shadow hover:bg-gray-800">
                  Print
                </button>
              </div>
            </div>
            <ol className="space-y-4 text-gray-700">
              <li><strong>1.</strong> Preheat oven to 375°F.</li>
              <li><strong>2.</strong> Roll out pie dough and place it in a pie pan. Decorate edges as desired.</li>
              <li><strong>3.</strong> Add apple slices to a large bowl. In a separate bowl, mix cream, sugars, flour, vanilla, and cinnamon. Pour over apples, then transfer to pie shell.</li>
              <li><strong>4.</strong> For the topping: In a food processor (or by hand), mix butter, flour, sugar, pecans, and salt. Mix until combined, then sprinkle over apples.</li>
              <li><strong>5.</strong> Attach foil to edges and place a flat foil sheet on top. Bake at 375°F for 1 hour. Remove foil for the last 15-20 minutes to allow browning.</li>
              <li><strong>6.</strong> Remove from oven when pie is bubbly and golden brown.</li>
              <li><strong>7.</strong> Serve warm with whipped cream, hard sauce, or ice cream.</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecipePage;

