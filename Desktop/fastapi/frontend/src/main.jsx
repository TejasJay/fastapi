// Import StrictMode from React - enables additional development checks and warnings for better code quality
import { StrictMode } from 'react'
// Import createRoot from react-dom/client - modern React 18+ API for rendering React components to the DOM
import { createRoot } from 'react-dom/client'
// Import global CSS styles that apply to the entire application
import './index.css'
// Import the main App component that contains all the application logic and routing
import App from './App.jsx'

// Get the root DOM element (div with id="root" from index.html) and create a React root
// This is where the entire React application will be rendered
createRoot(document.getElementById('root')).render(
  // StrictMode is a React wrapper that helps identify potential problems in the application
  // It activates additional checks and warnings for its descendants during development
  <StrictMode>
    {/* Render the main App component - this is the root component of the entire application */}
    <App />
  </StrictMode>,
)
