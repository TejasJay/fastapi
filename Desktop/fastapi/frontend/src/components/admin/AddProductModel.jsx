// Import React and hooks - useState for managing component state, useEffect for side effects
import React, { useState , useEffect } from "react";
// Import ProductApi to create products via the backend API
import ProductApi from "../../api/ProductApi.jsx";
// Import CategoryApi to fetch categories for the category dropdown
import CategoryApi from "../../api/CategoryApi.jsx";

// Define the AddProductModal functional component - modal dialog for creating new products
// Receives props: isOpen (boolean), onClose (callback), onSuccess (callback)
function AddProductModal({ isOpen, onClose, onSuccess }) {
  // State for storing the list of categories - initialized as empty array
  // setCategories function updates the categories array when data is fetched
  const [categories, setCategories] = useState([]);
  // State for storing product form data - initialized with empty string values
  // setProductData function updates the product data object when user types in form fields
  const [productData, setProductData] = useState({
    name: '',           // Product name input value
    description: '',    // Product description input value
    price: '',          // Product price input value (as string from input)
    category_id: '',    // Selected category ID (as string from select)
  });

  // useEffect hook runs when isOpen prop changes (when modal opens/closes)
  // Dependency array [isOpen] means this effect runs whenever modal visibility changes
  useEffect(() => {
    // Only load categories when modal is open (optimization - don't fetch when closed)
    if (isOpen) {
      // Define async function to fetch categories from the API
      const loadCategories = async () => {
        // Wrap API call in try-catch to handle errors gracefully
        try {
          // Call API to fetch all categories from the backend
          const res = await CategoryApi.fetchCategory();
          // Update categories state with the fetched category data
          setCategories(res.data);
          // Set a default category if available - pre-selects first category in dropdown
          if (res.data.length > 0) {
            // Update productData state, preserving existing values and setting default category_id
            // parseInt converts category ID from string to integer
            setProductData(pd => ({ ...pd, category_id: parseInt(res.data[0].id) }));
          }
        } catch (error) {
          // Log error to console if API call fails (for debugging)
          console.error("Failed to load categories:", error);
          // Handle category loading error, maybe show a message to the user
        }
      };
      // Call the async function to load categories when modal opens
      loadCategories();
    }
  }, [isOpen]); // Dependency on isOpen - effect runs when modal opens/closes

  // Early return if modal is not open - don't render anything when closed
  // This prevents the modal from taking up space in the DOM when hidden
  if (!isOpen) return null;

  // Handler function for form input changes - updates productData state
  // Uses computed property names to update the correct field based on input name
  const handleChange = (e) => {
    // Destructure name and value from the event target (the input element)
    const { name, value } = e.target;
    // Update productData state - spread previous values and update the changed field
    // [name] uses computed property name to dynamically set the field (name, description, etc.)
    setProductData(prev => ({ ...prev, [name]: value }));
  };

  // Async function that handles form submission when user clicks Create Product button
  const handleSubmit = async (e) => {
    // Prevent default form submission behavior (page reload)
    e.preventDefault();
    // Wrap API call in try-catch to handle errors gracefully
    try {
      // Send productData directly, without the extra 'productData' key
      // Call ProductApi to create a new product with the form data
      await ProductApi.createProduct({
        // Spread all productData fields into the request object
        ...productData,
        // Convert price from string to float number (parseFloat handles decimal values)
        price: parseFloat(productData.price),
        // Convert category_id from string to integer (parseInt with base 10)
        // Ensure category_id is an integer as required by the backend API
        category_id: parseInt(productData.category_id, 10) // Ensure category_id is an integer
      });
      // Show success alert to user when product is created
      alert('Product created successfully!');
      // Call onSuccess callback to refresh the product count in parent component
      onSuccess();
      // Call onClose callback to close the modal after successful creation
      onClose();
    } catch (error) {
      // Log error to console if API call fails (for debugging)
      console.error('Failed to create product:', error);
      // Log more specific error details if available from the backend
      // Check if error response contains validation error details
      if (error.response && error.response.data && error.response.data.detail) {
        // Log validation errors to console for debugging
        console.error("Validation errors:", error.response.data.detail);
        // Show user-friendly error message with all validation errors
        // Map error details to messages and join them with commas
        alert(`Failed to create product: ${error.response.data.detail.map(err => err.msg).join(", ")}`);
      } else {
        // Show generic error message if no specific error details available
        alert('Failed to create product. Please check console for details.');
      }
    }
  };

  // Return JSX that renders the modal dialog
  return (
    // Modal backdrop - dark overlay that covers the entire screen
    <div className="modal-backdrop">
      {/* Modal content container - the actual dialog box */}
      <div className="modal-content">
        {/* Modal title heading */}
        <h2>Add New Product</h2>
        {/* Form element - onSubmit triggers handleSubmit when form is submitted */}
        <form onSubmit={handleSubmit}>
          {/* Category dropdown select - allows user to select product category */}
          <select name="category_id" value={productData.category_id} onChange={handleChange} required>
            {/* Default disabled option - prompts user to select a category */}
            <option value="" disabled>Select a Category</option>
            {/* Map over categories array to render an option for each category */}
            {/* key prop is required by React for list items - uses category ID as unique identifier */}
            {categories.map(cat => (
              // Individual category option - value is category ID, display is category name
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
          {/* Product name input field - controlled input bound to productData.name */}
          <input name="name" value={productData.name} onChange={handleChange} placeholder="Product Name" required />
          {/* Product description textarea - controlled input bound to productData.description */}
          <textarea name="description" value={productData.description} onChange={handleChange} placeholder="Description" required />
          {/* Product price input - type="number" allows only numeric input */}
          {/* Controlled input bound to productData.price */}
          <input type="number" name="price" value={productData.price} onChange={handleChange} placeholder="Price" required />
          {/* Container for form action buttons */}
          <div className="modal-actions">
            {/* Submit button - triggers form submission and handleSubmit function */}
            <button type="submit">Create Product</button>
            {/* Cancel button - closes the modal without submitting */}
            {/* type='button' prevents form submission when clicked */}
            <button type="button" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Export the AddProductModal component so it can be imported and used in AdminDashboard
export default AddProductModal;