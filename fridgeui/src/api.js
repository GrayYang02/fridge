
import axios from 'axios';
import { ACCESS_TOKEN } from './constants';

const api = axios.create({
baseURL: process.env.REACT_APP_API_URL,
})

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);
export default api;

const API_BASE_URL = "http://127.0.0.1:8000/demo"; 
const API_BASE_URL_fri = "http://127.0.0.1:8000/demo/fridge"; 

export async function fetchFridgeItems(page = 1, pageSize = 10, sortBy = "create_time_desc") {
  try {
    const response = await fetch(`${API_BASE_URL_fri}/food_list/?page=${page}&page_size=${pageSize}&sort_by=${sortBy}`);
    if (!response.ok) {
      throw new Error("Failed to fetch fridge items");
    }
    const data = await response.json();
    return data.foods || [];
  } catch (error) {
    console.error("Error fetching fridge items:", error);
    return [];
  }
}

export async function addFridgeItem(item) {
  try {
    const response = await fetch(`${API_BASE_URL_fri}/add_food/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: item.name,
        user_id: item.user_id,
        add_time: item.add_time,
        expire_time: item.expire_time,
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to add fridge item");
    }
    return await response.json();
  } catch (error) {
    console.error("Error adding fridge item:", error);
    return null;
  }
}

export async function deleteFridgeItem(food_id) {
  try {
    const response = await fetch(`${API_BASE_URL_fri}/delete_food/`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ food_id }),
    });

// export const fetchFridgeItems = async () => {
//   try {
//     const response = await fetch(API_URL);
//     if (!response.ok) {
//       throw new Error("Failed to fetch fridge items");
//     }
//     return await response.json();
//   } catch (error) {
//     console.error("Error fetching fridge items:", error);
//     return [];
//   }
// };


    if (!response.ok) {
      throw new Error("Failed to delete fridge item");
    }
    return await response.json();
  } catch (error) {
    console.error("Error deleting fridge item:", error);
    return null;
  }
}
