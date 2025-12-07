// Import the configured axios instance with base URL from ApiService
import api from "./ApiService.jsx";

// Create a UserApi object that contains all user-related API methods
// This centralizes all user authentication and user management API calls
const UserApi = {
  // Login method: authenticates a user with username and password
  // Returns a promise that resolves with the authentication token
  login: (username, password) => {
    // Create a FormData object - required for OAuth2 password flow (form-urlencoded)
    // This format is needed because the backend expects form data, not JSON
    const formData = new FormData();
    // Append username to the form data - this will be sent as "username=value"
    formData.append("username", username);
    // Append password to the form data - this will be sent as "password=value"
    formData.append("password", password);
    // Make a POST request to the token endpoint to authenticate and get JWT token
    // The endpoint returns an access_token that will be stored in sessionStorage
    return api.post("/api/v1/users/token", formData);
  },
  // getSession method: retrieves the current user's session information
  // Requires a JWT token to authenticate the request
  getSession: (token) =>
    // Make a GET request to fetch the current user's session data (username, role, etc.)
    api.get("/api/v1/users/my_session/", {
      // Include the JWT token in the Authorization header using Bearer token format
      // This tells the backend which user is making the request
      headers: { Authorization: `Bearer ${token}` },
    }),
  // signup method: creates a new user account with username and password
  // Returns a promise that resolves when the user is successfully created
  signup: (username, password) =>
    // Make a POST request to create a new user account
    // Sends username and password as JSON in the request body
    api.post("/api/v1/users/", { username, password }),
};

// Export the UserApi object so it can be imported and used in Login and Signup components
export default UserApi;