// Import React library - required for creating React components
import React from "react";
// Import NavLink from react-router-dom - a special Link component that adds active styling when the route is active
import { NavLink } from 'react-router-dom';

// Define the Navbar functional component - displays the navigation bar at the top of every page
function Navbar(){
    // Return JSX that renders the navigation bar structure
    return (
        // nav element with "navbar" class - the main container for the navigation bar
        <nav className="navbar">
        {/* div with "nav-brand" class - displays the application name/logo */}
        <div className="nav-brand">
            {/* Application brand name displayed in the navigation bar */}
            E-Com-react
        </div>
        {/* div with "nav-links" class - container for navigation links */}
        <div className="nav-links">
            {/* NavLink to home page - automatically gets "active" class when route matches "/" */}
            {/* NavLink provides client-side navigation without full page reload */}
            <NavLink to="/">Customer View</NavLink>
            {/* NavLink to admin page - automatically gets "active" class when route matches "/admin" */}
            {/* Clicking this navigates to the admin dashboard */}
            <NavLink to="/admin">Admin View</NavLink>
        </div>
        </nav>
    );
}

// Export the Navbar component so it can be imported and used in App.jsx
export default Navbar;