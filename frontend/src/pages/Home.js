import React, { useContext, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { DataContext } from '../App'; 
import { useEffect } from 'react';
import './home.css';

const Home = () => {
  const navigate = useNavigate();
  
  // Accessing flaskData, loading, and error from context
  const { flaskData, loading, error } = useContext(DataContext);

  // Refs for scroll sections
  const worldRef = useRef(null);
  const internalRef = useRef(null);
  const usRef = useRef(null);

  const scrollToSection = (ref) => {
    window.scrollTo({
      top: ref.current.offsetTop - 100,
      behavior: 'smooth'
    });
  };

  // Transform the data
  const transformData = (data) => {
    if (!data) return [];
    return Object.values(data).map((article) => ({
      tag: article.subtopic || "General",
      title: article.title,
      description: getFirstWords(article.content, 30), // Get the first 40 words
      text: article.content,
      image: "https://via.placeholder.com/150", // Placeholder for image, update as needed
      time: formatTime(article.date),
      topic: article.topic // Ensure topic is included
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

  // Check if the data is loading or if there's an error
  if (loading) return <p>Data is loading...</p>

  if (error) return <p>Error: {error}</p>;

  // Transform the data only if it's available
  const newsData = flaskData ? transformData(flaskData) : [];

  const worldNews = newsData.filter(news => news.topic !== "Internal Affairs" && news.topic !== "United States").slice(0, 4);
  const internalNews = newsData.filter(news => news.topic === "Internal Affairs").slice(0, 4);
  const usNews = newsData.filter(news => news.topic === "United States").slice(0, 4);

  // Handle article click
  const handleArticleClick = (article) => {
    navigate('/article', { state: { article } });
  };

  return (
    <div className="home">
      {/* Section Links at the top-right */}
      <div className="first-content-container">
        <h2 className="section-title">Happening Now</h2>
        <div className="section-links">
          <span onClick={() => scrollToSection(worldRef)}>World</span>
          <span onClick={() => scrollToSection(internalRef)}>Internal Affairs</span>
          <span onClick={() => scrollToSection(usRef)}>United States</span>
        </div>
      </div>

      {/* World Section */}
      <section ref={worldRef} className="news-section">
        <h3 className="sub-header">World</h3>
        <div className="news-grid">
          {worldNews.map((news, index) => (
            <div
              key={index}
              className="news-card"
              onClick={() => handleArticleClick(news)}
            >
              <div className="top-content">
                <div className="top-text-container">
                  <div className="tag">{news.tag}</div>
                  <h4 className="news-title">{news.title}</h4>
                </div>
                <div className="image-container">
                  <img
                    src={news.image}
                    alt={news.title}
                    className="news-image"
                  />
                </div>
              </div>
              <div className="bottom-container">
              <p className="news-description">{news.description}</p>
              </div>
              <p className="news-time">{news.time}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Internal Affairs Section */}
      <section ref={internalRef} className="news-section">
        <h3 className="sub-header">Internal Affairs</h3>
        <div className="news-list">
            {internalNews.map((news, index) => (
              <div
                key={index}
                onClick={() => handleArticleClick(news)}
              >
              <div className="news-item">
                <div className="section-tag">{news.tag}</div>
                <div className="internal-header">{news.title}</div>
                <div className="internal-description">{news.description}</div>
                {/* <p className="internal-time">{news.time}</p> */}
              </div>
              </div>
            ))}
          </div>
      </section>

       {/* Internal Affairs Section */}
       <section ref={usRef} className="news-section">
        <h3 className="sub-header">United States</h3>
        <div className="news-list">
            {usNews.map((news, index) => (
              <div
                key={index}
                onClick={() => handleArticleClick(news)}
              >
              <div className="news-item">
                <div className="section-tag">{news.tag}</div>
                <div className="internal-header">{news.title}</div>
                <div className="internal-description">{news.description}</div>
                {/* <p className="internal-time">{news.time}</p> */}
              </div>
              </div>
            ))}
          </div>
      </section>
    </div>
  );
};

export default Home;
