import React from "react";
import { NavLink } from 'react-router-dom';

function Navbar(){
    return (
        <nav className="navbar">
        <div className="nav-brand">
            E-Com-react
        </div>
        <div className="nav-links">
            <NavLink to="/">Customer View</NavLink>
            <NavLink to="/admin">Admin View</NavLink>
        </div>
        </nav>
    );
}

export default Navbar;