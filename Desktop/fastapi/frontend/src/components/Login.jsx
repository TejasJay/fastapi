// Import React and useState hook - useState allows component to manage local state
import React, { useState } from "react";
// Import useNavigate and useLocation hooks from react-router-dom
// useNavigate: programmatically navigate to different routes
// useLocation: access location state passed from other routes (e.g., signup success message)
import { useNavigate, useLocation } from "react-router-dom";
// Import UserApi to make authentication API calls
import UserApi from "../api/UserApi.jsx";

// Define the Login functional component - handles user authentication
function Login() {
  // State for username input field - initialized as empty string
  // setUsername function updates the username state value
  const [username, setUsername] = useState("");
  // State for password input field - initialized as empty string
  // setPassword function updates the password state value
  const [password, setPassword] = useState("");
  // State for error messages - initialized as empty string
  // setError function updates the error message to display to user
  const [error, setError] = useState("");
  // Get navigate function from useNavigate hook - used to redirect after successful login
  const navigate = useNavigate();
  // Get location object from useLocation hook - contains route state and pathname
  const location = useLocation();

  // Async function that handles form submission when user clicks Login button
  const handleSubmit = async (e) => {
    // Prevent default form submission behavior (page reload)
    e.preventDefault();
    // Clear any previous error messages
    setError("");
    // Wrap API call in try-catch to handle errors gracefully
    try {
      // Call login API with username and password - returns JWT token
      const response = await UserApi.login(username, password);
      // Extract the access_token from the response data
      const token = response.data.access_token;
      // Store the JWT token in sessionStorage so it persists across page refreshes
      // sessionStorage is cleared when browser tab is closed
      sessionStorage.setItem("jwt_token", token);

      // Authenticate and get user role to determine where to redirect
      // Call getSession API to retrieve user information including role
      const sessionRes = await UserApi.getSession(token);
      // Extract the user's role (admin or customer) from the session response
      const role = sessionRes.data.role;

      // Redirect based on user role
      if (role === "admin") {
        // If user is admin, navigate to admin dashboard
        navigate("/admin");
      } else {
        // If user is customer, navigate to home page (which redirects to customer view)
        navigate("/");
      }
    } catch (err) {
      // If login fails, set error message to display to user
      // This catches network errors, invalid credentials, or server errors
      setError(`Invalid credentials or server error: ${err}`);
    }
  };

  // Return JSX that renders the login form
  return (
    // Container div with "container" class for consistent page styling
    <div className="container">
      {/* Page title heading */}
      <h1 className="page-title">Login</h1>
      {/* Conditionally render success message if redirected from signup page */}
      {/* location.state contains data passed via navigate() from Signup component */}
      {location.state && location.state.signupSuccess && (
        // Display green success message when user successfully signs up
        <p style={{ color: "green" }}>User created successfully. Please login.</p>
      )}
      {/* Login form - onSubmit triggers handleSubmit when form is submitted */}
      <form onSubmit={handleSubmit} style={{ maxWidth: 400, margin: "0 auto" }}>
        {/* Username input field */}
        <input
          type="text"
          placeholder="Username"
          // Controlled input - value is bound to username state
          value={username}
          // Update username state when user types in the input field
          onChange={e => setUsername(e.target.value)}
          // HTML5 validation - requires field to be filled before submission
          required
        />
        {/* Password input field */}
        <input
          type="password"
          placeholder="Password"
          // Controlled input - value is bound to password state
          value={password}
          // Update password state when user types in the input field
          onChange={e => setPassword(e.target.value)}
          // HTML5 validation - requires field to be filled before submission
          required
        />
        {/* Container for form action buttons */}
        <div className="modal-actions">
          {/* Submit button - triggers form submission and handleSubmit function */}
          <button type="submit">Login</button>
        </div>
        {/* Conditionally render error message if login fails */}
        {error && <p style={{ color: "red" }}>{error}</p>}
        {/* Link to signup page for users who don't have an account */}
        <p>
          Don't have an account? <a href="/signup">Signup</a>
        </p>
      </form>
    </div>
  );
}

// Export the Login component so it can be imported and used in App.jsx routing
export default Login;