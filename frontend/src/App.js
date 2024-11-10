import React, { createContext, useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Topics from './pages/Topics';
import ShareViewpoint from './pages/ShareViewpoint';
import Article from './pages/Article';
import Search from './pages/Search';
import MockCaptchaPage from './pages/MockCaptchaPage';
import './App.css';

// Create a Context to hold the fetched data
export const DataContext = createContext();

const App = () => {
  const [flaskData, setFlaskData] = useState(null);
  const [opinionsData, setOpinionsData] = useState(null); 
  const [topicsData, setTopicsData] = useState(null); 
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isVerified, setIsVerified] = useState(false);

  const fetchTopics = async () => {
    try {
      const response = await fetch('https://flaskapi-529120302078.europe-north1.run.app/get_topics');
      if (!response.ok) {
        throw new Error('Failed to fetch topics');
      }
      const data = await response.json();
      setTopicsData(data.data);
    } catch (err) {
      throw new Error(`Articles Fetch Error: ${err.message}`);
    }
  };

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
      await Promise.all([fetchArticles(), fetchOpinions(), fetchTopics()]);
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

  // Check if the user has already completed the CAPTCHA
  useEffect(() => {
    const verified = localStorage.getItem("isVerified") === "true";
    setIsVerified(verified);
  }, []);

  // If data is still loading or an error occurs, display loading/error message
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <DataContext.Provider value={{ flaskData, opinionsData, topicsData, loading, error }}>
      <Router>
        <div className="App">
          <Navbar />
          <Routes>
            {/* Display the CAPTCHA page only if the user has not verified yet */}
            {!isVerified ? (
              <Route
                path="/"
                element={<MockCaptchaPage setIsVerified={setIsVerified} />}
              />
            ) : (
              <Route path="/" element={<Navigate to="/home" />} />
            )}
            <Route path="/home" element={<Home />} />
            <Route path="/topics" element={<Topics />} />
            <Route path="/share" element={<ShareViewpoint />} />
            <Route path="/article" element={<Article />} />
            <Route path="/search" element={<Search />} />
          </Routes>
        </div>
      </Router>
    </DataContext.Provider>
  );
};

export default App;
