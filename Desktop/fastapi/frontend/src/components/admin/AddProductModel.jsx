import React, { useState , useEffect } from "react";
import ProductApi from "../../api/ProductApi.jsx";
import CategoryApi from "../../api/CategoryApi.jsx";

function AddProductModal({ isOpen, onClose, onSuccess }) {
  const [categories, setCategories] = useState([]);
  const [productData, setProductData] = useState({
    name: '',
    description: '',
    price: '',
    category_id: '',
  });

  useEffect(() => {
    if (isOpen) {
      const loadCategories = async () => {
        try {
          const res = await CategoryApi.fetchCategory();
          setCategories(res.data);
          // Set a default category if available
          if (res.data.length > 0) {
            setProductData(pd => ({ ...pd, category_id: parseInt(res.data[0].id) }));
          }
        } catch (error) {
          console.error("Failed to load categories:", error);
          // Handle category loading error, maybe show a message to the user
        }
      };
      loadCategories();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProductData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Send productData directly, without the extra 'productData' key
      await ProductApi.createProduct({
        ...productData,
        price: parseFloat(productData.price),
        category_id: parseInt(productData.category_id, 10) // Ensure category_id is an integer
      });
      alert('Product created successfully!');
      onSuccess();
      onClose();
    } catch (error) {
      console.error('Failed to create product:', error);
      // Log more specific error details if available from the backend
      if (error.response && error.response.data && error.response.data.detail) {
        console.error("Validation errors:", error.response.data.detail);
        alert(`Failed to create product: ${error.response.data.detail.map(err => err.msg).join(", ")}`);
      } else {
        alert('Failed to create product. Please check console for details.');
      }
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-content">
        <h2>Add New Product</h2>
        <form onSubmit={handleSubmit}>
          <select name="category_id" value={productData.category_id} onChange={handleChange} required>
            <option value="" disabled>Select a Category</option>
            {categories.map(cat => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
          <input name="name" value={productData.name} onChange={handleChange} placeholder="Product Name" required />
          <textarea name="description" value={productData.description} onChange={handleChange} placeholder="Description" required />
          <input type="number" name="price" value={productData.price} onChange={handleChange} placeholder="Price" required />
          <div className="modal-actions">
            <button type="submit">Create Product</button>
            <button type="button" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddProductModal;