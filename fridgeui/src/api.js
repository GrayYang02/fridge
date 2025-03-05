import axios from "axios";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./constants";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

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

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response.status === 401 && !originalRequest._retry) {
        
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem(REFRESH_TOKEN);
        if (!refreshToken) throw new Error("No refresh token");

        const res = await axios.post("/core/token/refresh/", {
          refresh: refreshToken,
        });

        localStorage.setItem(ACCESS_TOKEN, res.data.access);

        originalRequest.headers["Authorization"] = `Bearer ${res.data.access}`;
        return api(originalRequest);
      } catch (err) {
        console.error("Refresh token failed:", err);
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
        window.location.href = "/login";
        return Promise.reject(error);
      }
    }

    return Promise.reject(error);
  }
);

export default api;

const API_BASE_URL_FRIDGE = "/core/fridge";

const API_BASE_URL = "http://127.0.0.1:8000/demo"; // Django backend URL
const API_BASE_URL_fri = "http://127.0.0.1:8000/demo/fridge";

export async function fetchFridgeItems(
  page = 1,
  pageSize = 10,
  sortBy = "create_time_desc",
  searchTerm = "",
  isexp = null
) {
  try {
    console.log(localStorage.getItem("access"));

    const response = await api.get(`${API_BASE_URL_FRIDGE}/food_list/`, {
      params: {
        page,
        page_size: pageSize,
        sort_by: sortBy,
        keyword: searchTerm,
        is_expire: isexp,
      },
    });

    return response.data || { total: 0, foods: [] }; // 确保返回对象格式一致
  } catch (error) {
    console.error("Error fetching fridge items:", error);
    return { total: 0, foods: [] }; // 出错时返回默认值，防止前端崩溃
  }
}

export async function addFridgeItem(item) {
  try {
    const response = await api.post(`${API_BASE_URL_FRIDGE}/add_food/`, {
      name: item.name,
      user_id: item.user_id,
      add_time: item.add_time,
      expire_time: item.expire_time,
      tag: item.tag,
    });
    return response.data;
  } catch (error) {
    console.error("Error adding fridge item:", error);
    return null;
  }
}

// delete
export async function deleteFridgeItem(food_id) {
  try {
    const response = await api.delete(`${API_BASE_URL_FRIDGE}/delete_food/`, {
      data: { food_id },
    });
    return response.data;

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

    // if (!response.ok) {
    //   throw new Error("Failed to delete fridge item");
    // }
    // return await response.json();
    // >>>>>>> main
  } catch (error) {
    console.error("Error deleting fridge item:", error);
    return null;
  }
}
export async function fetchFoodTags() {
  try {
    const response = await api.get(`${API_BASE_URL_FRIDGE}/food_tags/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching food tags:", error);
    return {};
  }
}
