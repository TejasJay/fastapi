// Import React and hooks - useState for state, useEffect for side effects, useCallback for memoization
import React, { useState, useEffect, useCallback } from 'react';
// Import CategoryApi to fetch categories from the backend API
import CategoryApi from "../../api/CategoryApi.jsx";
// Import ProductApi to fetch products from the backend API
import ProductApi from "../../api/ProductApi.jsx";
// Import AddCategoryModal component - modal dialog for creating new categories
import AddCategoryModal from "./AddCategoryModel.jsx"
// Import AddProductModal component - modal dialog for creating new products
import AddProductModal from "./AddProductModel.jsx";

// Define the AdminDashboard functional component - main page for admin users
function AdminDashboard() {
  // State for storing the total number of categories - initialized as 0
  // setCategoryCount function updates the category count when data is fetched
  const [categoryCount, setCategoryCount] = useState(0);
  // State for storing the total number of products - initialized as 0
  // setProductCount function updates the product count when data is fetched
  const [productCount, setProductCount] = useState(0);
  // State for controlling visibility of Add Category modal - initialized as false (closed)
  // setCategoryModalOpen function opens/closes the category modal
  const [isCategoryModalOpen, setCategoryModalOpen] = useState(false);
  // State for controlling visibility of Add Product modal - initialized as false (closed)
  // setProductModalOpen function opens/closes the product modal
  const [isProductModalOpen, setProductModalOpen] = useState(false);

  // useCallback memoizes the function to prevent unnecessary re-renders
  // Empty dependency array [] means this function is created once and never changes
  const updateCounts = useCallback(async () => {
    // Wrap API calls in try-catch to handle errors gracefully
    try {
      // Fetch all categories from the backend API
      const catRes = await CategoryApi.fetchCategory();
      // Fetch all products from the backend API
      const prodRes = await ProductApi.fetchAllProducts();
      // Update category count with the length of categories array
      setCategoryCount(catRes.data.length);
      // Update product count with the length of products array
      setProductCount(prodRes.data.length);
    } catch (error) {
      // Log error to console if API calls fail (for debugging)
      console.error("Failed to update counts:", error);
    }
  }, []); // Empty dependency array - function is memoized and never changes

  // useEffect hook runs after component mounts and when updateCounts changes
  // Since updateCounts is memoized, this effect runs only once on mount
  useEffect(() => {
    // Call updateCounts to fetch and display initial counts when component mounts
    updateCounts();
  }, [updateCounts]); // Dependency on updateCounts - runs when updateCounts changes (only once)

  // Return JSX that renders the admin dashboard
  return (
    <div>
      {/* Page title heading */}
      <h1 className="page-title">Admin Dashboard</h1>
      {/* Container for dashboard statistics cards */}
      <div className="dashboard-cards">
        {/* Card displaying total number of categories */}
        <div className="dashboard-card">
          {/* Card title */}
          <h2>Total Categories</h2>
          {/* Display the category count value */}
          <p>{categoryCount}</p>
        </div>
        {/* Card displaying total number of products */}
        <div className="dashboard-card">
          {/* Card title */}
          <h2>Total Products</h2>
          {/* Display the product count value */}
          <p>{productCount}</p>
        </div>
      </div>
      {/* Container for admin action buttons */}
      <div className="admin-actions">
        {/* Button to open Add Category modal - onClick sets modal state to true (open) */}
        <button onClick={() => setCategoryModalOpen(true)}>Add Category</button>
        {/* Button to open Add Product modal - onClick sets modal state to true (open) */}
        <button onClick={() => setProductModalOpen(true)}>Add Product</button>
      </div>

      {/* AddCategoryModal component - renders modal dialog for creating categories */}
      {/* isOpen prop controls modal visibility based on isCategoryModalOpen state */}
      {/* onClose prop callback closes the modal by setting state to false */}
      {/* onSuccess prop callback refreshes counts after successful category creation */}
      <AddCategoryModal
        isOpen={isCategoryModalOpen}
        onClose={() => setCategoryModalOpen(false)}
        onSuccess={updateCounts}
      />
      {/* AddProductModal component - renders modal dialog for creating products */}
      {/* isOpen prop controls modal visibility based on isProductModalOpen state */}
      {/* onClose prop callback closes the modal by setting state to false */}
      {/* onSuccess prop callback refreshes counts after successful product creation */}
      <AddProductModal
        isOpen={isProductModalOpen}
        onClose={() => setProductModalOpen(false)}
        onSuccess={updateCounts}
      />
    </div>
  );
}

// Export the AdminDashboard component so it can be imported and used in App.jsx routing
export default AdminDashboard;