// Import React and useState hook - useState allows component to manage local state
import React, { useState } from "react";
// Import useNavigate hook from react-router-dom - programmatically navigate to different routes
import { useNavigate } from "react-router-dom";
// Import UserApi to make user registration API calls
import UserApi from "../api/UserApi.jsx";

// Define the Signup functional component - handles new user registration
function Signup() {
  // State for username input field - initialized as empty string
  // setUsername function updates the username state value
  const [username, setUsername] = useState("");
  // State for password input field - initialized as empty string
  // setPassword function updates the password state value
  const [password, setPassword] = useState("");
  // State for error messages - initialized as empty string
  // setError function updates the error message to display to user
  const [error, setError] = useState("");
  // Get navigate function from useNavigate hook - used to redirect after successful signup
  const navigate = useNavigate();

  // Async function that handles form submission when user clicks Signup button
  const handleSubmit = async (e) => {
    // Prevent default form submission behavior (page reload)
    e.preventDefault();
    // Clear any previous error messages
    setError("");
    // Wrap API call in try-catch to handle errors gracefully
    try {
      // Call signup API with username and password - creates new user account
      // This sends POST request to backend to register the new user
      await UserApi.signup(username, password);
      // If signup succeeds, navigate to login page
      // Pass state object with signupSuccess flag so Login component can show success message
      navigate("/login", { state: { signupSuccess: true } });
    } catch (err) {
      // If signup fails (e.g., username already exists), set error message
      // This catches network errors, validation errors, or duplicate username errors
      setError(`Signup failed. Try a different username. ${err}`);
    }
  };

  // Return JSX that renders the signup form
  return (
    // Container div with "container" class for consistent page styling
    <div className="container">
      {/* Page title heading */}
      <h1 className="page-title">Signup</h1>
      {/* Signup form - onSubmit triggers handleSubmit when form is submitted */}
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
          <button type="submit">Signup</button>
        </div>
        {/* Conditionally render error message if signup fails */}
        {error && <p style={{ color: "red" }}>{error}</p>}
        {/* Link to login page for users who already have an account */}
        <p>
          Already have an account? <a href="/login">Login</a>
        </p>
      </form>
    </div>
  );
}

// Export the Signup component so it can be imported and used in App.jsx routing
export default Signup;