// Import the configured axios instance with base URL from ApiService
import api from "./ApiService.jsx";

// Helper function to get the authentication header with JWT token
// This function retrieves the token from sessionStorage and formats it for the Authorization header
const getAuthHeader = () => {
    // Retrieve the JWT token from browser's sessionStorage
    // sessionStorage persists data only for the current browser tab/session
    const token = sessionStorage.getItem("jwt_token");
    // If token exists, return Authorization header with Bearer token format
    // If no token exists, return empty object (no auth header)
    return token ? { Authorization: `Bearer ${token}` } : {};
}

// Create a ProductApi object that contains all product-related API methods
// This centralizes all product management API calls
const ProductApi = {
    // fetchAllProducts method: retrieves all products from the backend
    // Includes authentication header to ensure only authenticated users can access products
    // Returns a promise that resolves with an array of all product objects
    fetchAllProducts: () => api.get("/api/v1/products", {headers: getAuthHeader()}),
    // createProduct method: creates a new product with the provided product data
    // Takes productData object containing name, description, price, and category_id
    // Includes authentication header to ensure only authenticated users can create products
    // Returns a promise that resolves when the product is successfully created
    createProduct: (productData) => api.post("/api/v1/products", productData, {headers: getAuthHeader()}),
};

// Export the ProductApi object so it can be imported and used in components
export default ProductApi;