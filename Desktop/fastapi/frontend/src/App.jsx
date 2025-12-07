// Import React library - required for creating React components
import React from 'react';
// Import routing components from react-router-dom
// BrowserRouter (aliased as Router): provides routing context for the entire app
// Routes: container for route definitions
// Route: defines a single route with path and component
// Navigate: programmatically redirects to a different route
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// Import Navbar component - displays navigation bar on all pages
import Navbar from './components/Navbar';
// Import AdminDashboard component - main page for admin users
import AdminDashboard from './components/admin/AdminDashboard.jsx';
// Import CustomerPage component - main page for customer users to browse products
import CustomerPage from './components/customer/CustomerPage.jsx';
// Import Login component - handles user authentication
import Login from './components/Login.jsx';
// Import Signup component - handles new user registration
import Signup from './components/Signup.jsx';
// Import api instance - configured axios instance with base URL
import api from './api/ApiService.jsx';
// Import App.css - styles specific to the App component
import './App.css'

// HomeRedirect component: Redirects "/" to login or dashboard based on JWT token and user role
// This component checks if user is authenticated and redirects to appropriate page
function HomeRedirect() {
  // State for storing the redirect destination - initialized as null (no redirect yet)
  // setRedirect function updates the redirect path when authentication check completes
  const [redirect, setRedirect] = React.useState(null);

  // useEffect hook runs after component mounts (when page loads)
  // Empty dependency array [] means this effect runs only once on mount
  React.useEffect(() => {
    // Retrieve JWT token from sessionStorage to check if user is logged in
    const token = sessionStorage.getItem("jwt_token");
    // If no token exists, user is not authenticated
    if (!token) {
      // Set redirect to login page for unauthenticated users
      setRedirect("/login");
      // Exit early - no need to check session if no token
      return;
    }
    // If token exists, verify it's valid and get user role
    // Make API call to get current user's session information
    api.get("/api/v1/users/my_session/", {
      // Include JWT token in Authorization header to authenticate the request
      headers: { Authorization: `Bearer ${token}` }
    })
      // If API call succeeds, check user role and redirect accordingly
      .then(res => {
        // Check if user role is "admin"
        if (res.data.role === "admin") {
          // Redirect admin users to admin dashboard
          setRedirect("/admin");
        } else {
          // Redirect non-admin users (customers) to customer page
          setRedirect("/customer");
        }
      })
      // If API call fails (invalid token, network error, etc.)
      .catch(() => {
        // Redirect to login page if authentication fails
        setRedirect("/login");
      });
  }, []); // Empty dependency array - effect runs only once on component mount

  // If redirect path is set, use Navigate component to redirect
  // replace prop replaces current history entry instead of adding new one
  if (redirect) return <Navigate to={redirect} replace />;
  // While checking authentication, show loading message
  return <div>Loading...</div>;
}

// AdminRoute component: Protects admin route - only allows admin users to access
// This is a Higher-Order Component pattern that wraps protected routes
function AdminRoute({ children }) {
  // State for storing authentication status - null means not checked yet
  // setAuth function updates auth status (true = admin, false = not admin)
  const [auth, setAuth] = React.useState(null);
  // State for loading status - true means authentication check is in progress
  // setLoading function updates loading status when check completes
  const [loading, setLoading] = React.useState(true);

  // useEffect hook runs after component mounts (when route is accessed)
  // Empty dependency array [] means this effect runs only once on mount
  React.useEffect(() => {
    // Retrieve JWT token from sessionStorage to check if user is logged in
    const token = sessionStorage.getItem("jwt_token");
    // If no token exists, user is not authenticated
    if (!token) {
      // Set auth to false (not authorized)
      setAuth(false);
      // Set loading to false (check complete)
      setLoading(false);
      // Exit early - no need to check session if no token
      return;
    }
    // If token exists, verify user role
    // Make API call to get current user's session information
    api.get("/api/v1/users/my_session/", {
      // Include JWT token in Authorization header to authenticate the request
      headers: { Authorization: `Bearer ${token}` }
    })
      // If API call succeeds, check if user is admin
      .then(res => {
        // Set auth to true only if user role is "admin"
        setAuth(res.data.role === "admin");
        // Set loading to false (check complete)
        setLoading(false);
      })
      // If API call fails (invalid token, network error, etc.)
      .catch(() => {
        // Set auth to false (not authorized)
        setAuth(false);
        // Set loading to false (check complete)
        setLoading(false);
      });
  }, []); // Empty dependency array - effect runs only once on component mount

  // While checking authentication, show loading message
  if (loading) return <div>Loading...</div>;
  // If user is not authorized (not admin), show access denied message
  if (!auth) return <div className="container"><h2>This page is for admin only.</h2></div>;
  // If user is authorized (admin), render the protected children components
  return children;
}

// CustomerRoute component: Protects customer route - only allows customer users to access
// This prevents admin users from accessing customer pages
function CustomerRoute({ children }) {
  // State for storing authentication status - null means not checked yet
  // setAuth function updates auth status (true = customer, false = not customer)
  const [auth, setAuth] = React.useState(null);
  // State for loading status - true means authentication check is in progress
  // setLoading function updates loading status when check completes
  const [loading, setLoading] = React.useState(true);

  // useEffect hook runs after component mounts (when route is accessed)
  // Empty dependency array [] means this effect runs only once on mount
  React.useEffect(() => {
    // Retrieve JWT token from sessionStorage to check if user is logged in
    const token = sessionStorage.getItem("jwt_token");
    // If no token exists, user is not authenticated
    if (!token) {
      // Set auth to false (not authorized)
      setAuth(false);
      // Set loading to false (check complete)
      setLoading(false);
      // Exit early - no need to check session if no token
      return;
    }
    // If token exists, verify user is not admin (must be customer)
    // Make API call to get current user's session information
    api.get("/api/v1/users/my_session/", {
      // Include JWT token in Authorization header to authenticate the request
      headers: { Authorization: `Bearer ${token}` }
    })
      // If API call succeeds, check if user is NOT admin (i.e., is customer)
      .then(res => {
        // Set auth to true only if user role is NOT "admin" (is customer)
        setAuth(res.data.role !== "admin");
        // Set loading to false (check complete)
        setLoading(false);
      })
      // If API call fails (invalid token, network error, etc.)
      .catch(() => {
        // Set auth to false (not authorized)
        setAuth(false);
        // Set loading to false (check complete)
        setLoading(false);
      });
  }, []); // Empty dependency array - effect runs only once on component mount

  // While checking authentication, show loading message
  if (loading) return <div>Loading...</div>;
  // If user is not authorized (is admin or not logged in), show access denied message
  if (!auth) return <div className="container"><h2>This page is for customers only.</h2></div>;
  // If user is authorized (customer), render the protected children components
  return children;
}

// App component: Main application component that sets up routing and renders the entire app
function App() {
  // Return JSX that renders the application structure
  return (
    // BrowserRouter (aliased as Router) - provides routing context for all child components
    // This enables React Router functionality throughout the app
    <Router>
      {/* Navbar component - displays navigation bar on all pages */}
      <Navbar />
      {/* Main content container with "container" class for consistent styling */}
      <main className='container'>
        {/* Routes container - defines all available routes in the application */}
        <Routes>
          {/* Home route "/" - redirects to appropriate page based on authentication */}
          <Route path="/" element={<HomeRedirect />} />
          {/* Login route "/login" - displays login form for user authentication */}
          <Route path="/login" element={<Login />} />
          {/* Signup route "/signup" - displays registration form for new users */}
          <Route path="/signup" element={<Signup />} />
          {/* Admin route "/admin" - protected route that only admin users can access */}
          <Route
            path="/admin"
            element={
              // AdminRoute wrapper checks if user is admin before rendering AdminDashboard
              <AdminRoute>
                {/* AdminDashboard component - only rendered if user is authenticated as admin */}
                <AdminDashboard />
              </AdminRoute>
            }
          />
          {/* Customer route "/customer" - protected route that only customer users can access */}
          <Route
            path="/customer"
            element={
              // CustomerRoute wrapper checks if user is customer before rendering CustomerPage
              <CustomerRoute>
                {/* CustomerPage component - only rendered if user is authenticated as customer */}
                <CustomerPage />
              </CustomerRoute>
            }
          />
        </Routes>
      </main>
    </Router>
  );
}

// Export the App component so it can be imported and used in main.jsx
export default App