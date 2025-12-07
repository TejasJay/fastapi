// Import React and hooks - useState for managing component state, useEffect for side effects
import React, { useState, useEffect } from 'react';
// Import ProductApi to fetch products from the backend API
import ProductApi from "../../api/ProductApi.jsx";
// Import CategoryList component - displays category filter buttons
import CategoryList from './CategoryList.jsx';
// Import ProductGrid component - displays products in a grid layout
import ProductGrid from './ProductGrid.jsx';

// Define the CustomerPage functional component - main page for customers to browse products
function CustomerPage() {
  // State for storing the list of products to display - initialized as empty array
  // setProducts function updates the products array when data is fetched
  const [products, setProducts] = useState([]);
  // State for the page title - initialized with default title
  // setTitle function updates the title when category filter changes
  const [title, setTitle] = useState('Our Star Products');

  // useEffect hook runs after component mounts (when page loads)
  // Empty dependency array [] means this effect runs only once on mount
  useEffect(() => {
    // Fetch all products on initial load
    // Define async function to fetch products from the API
    const loadAllProducts = async () => {
      // Wrap API call in try-catch to handle errors gracefully
      try {
        // Call API to fetch all products from the backend
        const response = await ProductApi.fetchAllProducts();
        // Update products state with the fetched product data
        setProducts(response.data);
      } catch (error) {
        // Log error to console if API call fails (for debugging)
        console.error("Failed to fetch products:", error);
      }
    };
    // Call the async function to load products when component mounts
    loadAllProducts();
  }, []); // Empty dependency array - effect runs only once on component mount

  // Handler function called when user selects a category from CategoryList
  // Takes category object as parameter (or null if "All" is selected)
  const handleCategorySelect = async (category) => {
    // Check if "All Products" was selected (category is null or undefined)
    if (!category) {
        // If "All" is selected or component mounts, fetch all products
        // Call API to fetch all products regardless of category
        const response = await ProductApi.fetchAllProducts();
        // Update products state with all products
        setProducts(response.data);
        // Update page title to default "Our Star Products"
        setTitle('Our Star Products');
    } else {
        // If a specific category is selected, fetch products for that category
        // Wrap API call in try-catch to handle errors gracefully
        try {
            // Call API to fetch products filtered by category ID
            // Note: This should use CategoryApi.fetchProductsByCategory, not ProductApi
            const response = await ProductApi.fetchProductsByCategory(category.id);
            // Update products state with filtered products
            setProducts(response.data);
            // Update page title to show selected category name
            setTitle(`Products in ${category.name}`);
        } catch (error) {
            // Log error to console if API call fails
            console.error("Failed to fetch products by category:", error);
            // Clear products array on error so user sees empty state instead of stale data
            setProducts([]); // Clear products on error
        }
    }
  };

  // Return JSX that renders the customer page layout
  return (
    <div>
      {/* Render CategoryList component - displays category filter buttons */}
      {/* Pass handleCategorySelect as callback prop so CategoryList can notify when category is selected */}
      <CategoryList onCategorySelect={handleCategorySelect} />
      {/* Page title that changes based on selected category */}
      <h1 className="page-title">{title}</h1>
      {/* Render ProductGrid component - displays products in a grid layout */}
      {/* Pass products array as prop so ProductGrid can render the product cards */}
      <ProductGrid products={products} />
    </div>
  );
}

// Export the CustomerPage component so it can be imported and used in App.jsx routing
export default CustomerPage;