const API_BASE_URL = "http://127.0.0.1:8000/demo";  // Django 后端 URL

// 获取冰箱食材列表
export async function fetchFridgeItems() {
  const response = await fetch(`${API_BASE_URL}/fridge/`);
  return response.json();
}

// 添加新食材
export async function addFridgeItem(item) {
  const response = await fetch(`${API_BASE_URL}/fridge/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(item),
  });
  return response.json();
}

// 删除食材
export async function deleteFridgeItem(id) {
  await fetch(`${API_BASE_URL}/fridge/${id}/`, {
    method: "DELETE",
  });
}
const API_URL = "http://127.0.0.1:8000/demo/fridge/";

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
