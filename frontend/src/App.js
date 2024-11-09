import React, { createContext, useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Topics from './pages/Topics';
import ShareViewpoint from './pages/ShareViewpoint';
import Article from './pages/Article';
import './App.css';

// Create a Context to hold the fetched data
export const DataContext = createContext();

const App = () => {
  const [flaskData, setFlaskData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Function to fetch data from Flask API
  const fetchData = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/data');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      setFlaskData(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  // Fetch data on component mount
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <DataContext.Provider value={{ flaskData, loading, error }}>
      <Router>
        <div className="App">
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/topics" element={<Topics />} />
            <Route path="/share" element={<ShareViewpoint />} />
            <Route path="/article" element={<Article />} />
          </Routes>
        </div>
      </Router>
    </DataContext.Provider>
  );
};

export default App;

