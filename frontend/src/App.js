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
  const [opinionsData, setOpinionsData] = useState(null); // New state for opinions
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Function to fetch data from the first endpoint
  const fetchArticles = async () => {
    try {
      const response = await fetch('https://flaskapi-529120302078.europe-north1.run.app/get_articles');
      if (!response.ok) {
        throw new Error('Failed to fetch articles');
      }
      const data = await response.json();
      setFlaskData(data.data);
    } catch (err) {
      throw new Error(`Articles Fetch Error: ${err.message}`);
    }
  };

  // Function to fetch data from the second endpoint
  const fetchOpinions = async () => {
    try {
      const response = await fetch('https://flaskapi-529120302078.europe-north1.run.app/get_opinions');
      if (!response.ok) {
        throw new Error('Failed to fetch opinions');
      }
      const data = await response.json();
      setOpinionsData(data.data);
    } catch (err) {
      throw new Error(`Opinions Fetch Error: ${err.message}`);
    }
  };

  // Combined function to fetch both sets of data
  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      await Promise.all([fetchArticles(), fetchOpinions()]);
    } catch (err) {
      setError(err.message);
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
    <DataContext.Provider value={{ flaskData, opinionsData, loading, error }}>
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
