import React from "react";
import RecipeListView from "./RecipeListView";

const ViewedView = () => {
  return (
    <RecipeListView
      title="Viewed Recipes"
      operationName="viewed"
    ></RecipeListView>
  );
};

export default ViewedView;
