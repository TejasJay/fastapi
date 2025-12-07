// Import the configured axios instance with base URL from ApiService
import api from "./ApiService.jsx";

// Create a CategoryApi object that contains all category-related API methods
// This centralizes all category management API calls
const CategoryApi = {
    // fetchCategory method: retrieves all categories from the backend
    // Returns a promise that resolves with an array of category objects
    fetchCategory: () => api.get("/api/v1/categories"),
    // createCategory method: creates a new category with the given name
    // Takes a category name as parameter and sends it to the backend
    // Returns a promise that resolves when the category is successfully created
    createCategory: (name) => api.post("/api/v1/categories", { name }),
    // fetchProductsByCategory method: retrieves all products that belong to a specific category
    // Takes a categoryId as parameter to filter products by category
    // Returns a promise that resolves with an array of products in that category
    fetchProductsByCategory: (categoryId) => api.get(`/api/v1/categories/${categoryId}`),
};

// Export the CategoryApi object so it can be imported and used in components
export default CategoryApi;