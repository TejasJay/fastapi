// Import axios library - a popular HTTP client for making API requests from JavaScript
import axios from 'axios';

// Create a configured axios instance with a base URL
// This instance will automatically prepend "http://localhost:8000" to all API requests
// This avoids repeating the base URL in every API call throughout the application
const api = axios.create({
    // Set the base URL for all API requests - points to the FastAPI backend server
    baseURL: "http://localhost:8000",
});

// Export the configured axios instance so it can be imported and used in other API files
// This ensures all API calls use the same base configuration
export default api;