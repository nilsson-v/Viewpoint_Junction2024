import React, { useRef, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css';

// Custom hook to fetch data from Flask API
const useFetchFlaskData = (apiUrl) => {
  const [flaskData, setFlaskData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Function to fetch data from Flask API
  const fetchData = async () => {
    try {
      const response = await fetch(apiUrl);
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
  }, [apiUrl]);

  return { flaskData, loading, error };
};

// Helper function to transform JSON data
const transformData = (data) => {
  if (!data) return [];
  return Object.values(data).map((article) => ({
    tag: article.subtopic || "General",
    title: article.title,
    description: getFirstWords(article.content, 100), // Get the first 50 words
    image: "https://via.placeholder.com/150", // Placeholder for image, update as needed
    time: formatTime(article.date)
  }));
};

// Helper function to get the first N words of a string
const getFirstWords = (text, wordCount) => {
  const words = text.split(' ');
  return words.slice(0, wordCount).join(' ') + (words.length > wordCount ? "..." : "");
};

// Helper function to format the timestamp
const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  const now = new Date();
  const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
  return diffInHours === 0 ? "Just now" : `${diffInHours} hours ago`;
};

const Home = () => {
  const navigate = useNavigate();

  // Fetching data from Flask API
  const { flaskData, loading, error } = useFetchFlaskData('http://127.0.0.1:5000/api/data');

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  // Transform the data only if it's available
  const newsData = flaskData ? transformData(flaskData) : [];

  const handleArticleClick = (article) => {
    navigate('/article', { state: { article } });
  };

  return (
    <div className="home">
      <h2 className="section-title">Happening Now</h2>
      <div className="news-grid">
        {newsData.map((news, index) => (
          <div 
            key={index} 
            className="news-card"
            onClick={() => handleArticleClick(news)}
          >
            <div className="tag">{news.tag}</div>
            <h4 className="news-title">{news.title}</h4>
            <p className="news-description">{news.description}</p>
            <img src={news.image} alt={news.title} className="news-image" />
            <p className="news-time">{news.time}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
