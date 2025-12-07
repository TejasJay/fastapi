// Import React and useState hook - useState allows component to manage local state
import React, { useState } from 'react';
// Import CategoryApi to create categories via the backend API
import CategoryApi from '../../api/CategoryApi';

// Define the AddCategoryModel functional component - modal dialog for creating new categories
// Receives props: isOpen (boolean), onClose (callback), onSuccess (callback)
function AddCategoryModel({isOpen, onClose, onSuccess}) {
    // State for category name input field - initialized as empty string
    // setName function updates the name state value
    const [name, setName] = useState('');
    // Early return if modal is not open - don't render anything when closed
    // This prevents the modal from taking up space in the DOM when hidden
    if (!isOpen) return null;

    // Async function that handles form submission when user clicks Submit button
    const handleSubmit = async (e) => {
        // Prevent default form submission behavior (page reload)
        e.preventDefault();
        // Wrap API call in try-catch to handle errors gracefully
        try {
            // Call CategoryApi to create a new category with the entered name
            // This sends POST request to backend to create the category
            await CategoryApi.createCategory(name);
            // Show success alert to user when category is created
            alert(`Category ${name} created successfully`);
            // Call onSuccess callback to refresh the category count in parent component
            onSuccess();
            // Call onClose callback to close the modal after successful creation
            onClose();
        } catch (error) {
            // Log error to console if API call fails (for debugging)
            console.error('Error creating category:', error);
            // Show error alert to user if category creation fails
            alert('Failed to create category. Please try again.');
        }
    };
    // Return JSX that renders the modal dialog
    return (
        // Modal backdrop - dark overlay that covers the entire screen
        // Clicking this area typically closes the modal (not implemented here)
        <div className='modal-backdrop'>
            {/* Modal content container - the actual dialog box */}
            <div className='modal-content'>
                {/* Modal title heading */}
                <h2>Add Category</h2>
                {/* Form element - onSubmit triggers handleSubmit when form is submitted */}
                <form onSubmit={handleSubmit}>
                    {/* Category name input field */}
                    <input 
                    type='text' 
                    placeholder='Category Name' 
                    // Controlled input - value is bound to name state
                    value={name} 
                    // Update name state when user types in the input field
                    onChange={(e) => setName(e.target.value)}
                    // HTML5 validation - requires field to be filled before submission
                    required
                    />
                    {/* Container for form action buttons */}
                    <div className='modal-actions'>
                        {/* Submit button - triggers form submission and handleSubmit function */}
                        <button type='submit'>Submit</button>
                        {/* Cancel button - closes the modal without submitting */}
                        {/* type='button' prevents form submission when clicked */}
                        <button type='button' onClick={onClose}>Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    );
};  
// Export the AddCategoryModel component so it can be imported and used in AdminDashboard
export default AddCategoryModel;