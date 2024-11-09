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
      // Update the URL to match where your Flask app is hosted
      const response = await fetch('https://flaskapi-529120302078.europe-north1.run.app/get_articles');
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      // Access the "data" object and set it as flaskData
      setFlaskData(data.articles); 
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

  // If data is still loading or an error occurs, display loading/error message
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

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
