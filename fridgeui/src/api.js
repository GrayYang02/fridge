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

const API_BASE_URL_FRIDGE = "/core/fridge";


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

    return response.data || { total: 0, foods: [] }; 
  } catch (error) {
    console.error("Error fetching fridge items:", error);
    return { total: 0, foods: [] }; 
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
      data: { food_id }
    });
    return response.data;

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