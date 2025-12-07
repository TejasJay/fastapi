// Import React and hooks - useState for managing component state, useEffect for side effects
import React, { useState, useEffect } from 'react';
// Import CategoryApi to fetch categories from the backend API
import CategoryApi from "../../api/CategoryApi.jsx";

// Define the CategoryList functional component - displays category filter buttons
// Receives onCategorySelect callback function as prop from parent component
function CategoryList({ onCategorySelect }) {
  // State for storing the list of categories - initialized as empty array
  // setCategories function updates the categories array when data is fetched
  const [categories, setCategories] = useState([]);

  // useEffect hook runs after component mounts (when page loads)
  // Empty dependency array [] means this effect runs only once on mount
  useEffect(() => {
    // Define async function to fetch categories from the API
    const loadCategories = async () => {
      // Wrap API call in try-catch to handle errors gracefully
      try {
        // Call API to fetch all categories from the backend
        const response = await CategoryApi.fetchCategory();
        // Update categories state with the fetched category data
        setCategories(response.data);
      } catch (error) {
        // Log error to console if API call fails (for debugging)
        console.error("Failed to fetch categories:", error);
      }
    };
    // Call the async function to load categories when component mounts
    loadCategories();
  }, []); // Empty dependency array - effect runs only once on component mount

  // Return JSX that renders the category filter buttons
  return (
    // Container div with "category-tabs" class for styling the category buttons
    <div className="category-tabs">
      {/* "All Products" button - shows all products regardless of category */}
      {/* onClick handler calls onCategorySelect with null to indicate "all categories" */}
      <button onClick={() => onCategorySelect(null)}>All Products</button>
      {/* Map over categories array to render a button for each category */}
      {/* key prop is required by React for list items - uses category ID as unique identifier */}
      {categories.map((cat) => (
        // Individual category button - clicking filters products by this category
        <button key={cat.id} onClick={() => onCategorySelect(cat)}>
          {/* Display the category name on the button */}
          {cat.name}
        </button>
      ))}
    </div>
  );
}

// Export the CategoryList component so it can be imported and used in CustomerPage
export default CategoryList;