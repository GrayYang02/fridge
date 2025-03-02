import React from "react";
import recipepic from "../assets/recipepic.png";
import RecipeListView from "./RecipeListView";

const CookedView = () => {
  return (
    <RecipeListView
      title="Cooked Recipes"
      operationName="cooked"
    ></RecipeListView>
  );
};

export default CookedView;
