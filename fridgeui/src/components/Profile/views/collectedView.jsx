import React from "react";
import RecipeListView from "./RecipeListView";

const CollectedView = () => {
  return (
    <RecipeListView
      title="Collected Recipes"
      operationName="collected"
    ></RecipeListView>
  );
};

export default CollectedView;
