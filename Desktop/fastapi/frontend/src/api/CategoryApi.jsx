import api from "./ApiService.jsx";

const CategoryApi = {
    fetchCategory: () => api.get("/api/v1/categories"),
    createCategory: (name) => api.post("/api/v1/categories", { name }),
    fetchProductsByCategory: (categoryId) => api.get(`/api/v1/categories/${categoryId}`),
};

export default CategoryApi;