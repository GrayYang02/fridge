import axios from 'axios';
import { ACCESS_TOKEN } from './constants';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

api.interceptors.request.use(
  (config) => {
    const token1 = localStorage.getItem(ACCESS_TOKEN);
    const token = localStorage.getItem('access'); 
    console.log('1111')

    console.log(token)

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

export async function fetchFridgeItems(page = 1, pageSize = 10, sortBy = "create_time_desc") {
  try {
    console.log('sdcfvgbhn')

    console.log(localStorage.getItem('access'))
    // console.log(config.headers.Authorization)
    const response = await api.get(`${API_BASE_URL_FRIDGE}/food_list/`, {
      params: { page, page_size: pageSize, sort_by: sortBy }
    });
    return response.data.foods || [];
  } catch (error) {
    console.error("Error fetching fridge items:", error);
    return [];
  }
}

export async function addFridgeItem(item) {
  try {
    const response = await api.post(`${API_BASE_URL_FRIDGE}/add_food/`, {
      name: item.name,
      user_id: item.user_id,
      add_time: item.add_time,
      expire_time: item.expire_time,
    });
    return response.data;
  } catch (error) {
    console.error("Error adding fridge item:", error);
    return null;
  }
}

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
