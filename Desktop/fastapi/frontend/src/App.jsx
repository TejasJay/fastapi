import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar'; 
import './App.css'

function CustomerView() {
  return <div><h1>Customer View</h1><p>Welcome to the customer view!</p></div>;
}

function AdminView() {
  return <div><h1>Admin View</h1><p>Welcome to the admin view!</p></div>;
}

function App() {
  return (
    <Router>
      <Navbar />
      <main className='container'>
        <Routes>
          <Route path='/' element={<CustomerView />} />  
          <Route path='/admin' element={<AdminView />} />  
        </Routes>
      </main>
    </Router>
  );
}

export default App