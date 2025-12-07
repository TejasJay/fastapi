import React, { useState } from 'react';
import CategoryApi from '../../api/CategoryApi';

function AddCategoryModel({isOpen, onClose, onSuccess}) {
    const [name, setName] = useState('');
    if (!isOpen) return null;

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await createCategory(name);
            alert(`Category ${name} created successfully`);
            onSuccess();
            onClose();
        } catch (error) {
            console.error('Error creating category:', error);
            alert('Failed to create category. Please try again.');
        }
    };
    return (
        <div className='modal-backdrop'>
            <div className='modal-content'>
                <h2>Add Category</h2>
                <form onSubmit={handleSubmit}>
                    <input 
                    type='text' 
                    placeholder='Category Name' 
                    value={name} 
                    onChange={(e) => setName(e.target.value)}
                    required
                    />
                    <div className='modal-actions'>
                        <button type='submit'>Submit</button>
                        <button type='button' onClick={onClose}>Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    );
};  
export default AddCategoryModel;