// Import React library - required for creating React components
import React from 'react';

// Define the ProductGrid functional component - displays products in a grid layout
// Receives products array as prop from parent component (CustomerPage)
function ProductGrid({ products }) {
  // Early return if products array is empty - show message instead of empty grid
  // This handles the case when no products are found or still loading
  if (!products.length) {
    // Return a paragraph element with message for empty state
    return <p>No products found.</p>;
  }

  // Return JSX that renders the product grid
  return (
    // Container div with "product-grid" class for CSS grid layout styling
    <div className="product-grid">
      {/* Map over products array to render a card for each product */}
      {/* key prop is required by React for list items - uses product ID as unique identifier */}
      {products.map((product) => (
        // Individual product card container with "product-card" class
        <div key={product.id} className="product-card">
          {/* Container for product information with "product-info" class */}
          <div className="product-info">
            {/* Product name displayed as heading level 3 */}
            <h3>{product.name}</h3>
            {/* Product description with "product-desc" class for styling */}
            <p className="product-desc">{product.description}</p>
            {/* Product price formatted to 2 decimal places with dollar sign */}
            {/* toFixed(2) ensures price always shows 2 decimal places (e.g., $19.99) */}
            <p className="product-price">${product.price.toFixed(2)}</p>
            {/* Product category name displayed as a span with "product-category" class */}
            {/* Accesses nested category object from product to get category name */}
            <span className="product-category">{product.category.name}</span>
          </div>
        </div>
      ))}
    </div>
  );
}

// Export the ProductGrid component so it can be imported and used in CustomerPage
export default ProductGrid;