import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './search.css';

const Search = () => {
  const navigate = useNavigate();

  const [flaskData, setFlaskData] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoadingSearch] = useState(false);
  const [error, setSearchError] = useState(null);

  // Function to handle search input changes
  const handleSearchChange = (event) => {
    setSearchQuery(event.target.value);
  };

  // Function to fetch data with a POST request to the Flask API
  const searchArticles = async (event) => {
    event.preventDefault();
    setLoadingSearch(true);
    setSearchError(null);

    try {
      // Make a POST request to your Flask backend
      const response = await fetch('https://flaskapi-529120302078.europe-north1.run.app/search_articles', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: searchQuery }) // Send the search query as payload
      });

      if (!response.ok) {
        throw new Error('Failed to fetch articles');
      }

      const data = await response.json();

      // Store the results in state
      setFlaskData(data.data || []);
    } catch (err) {
      setSearchError(err.message);
    } finally {
      setLoadingSearch(false);
    }
  };

  const getFirstWords = (text, wordCount) => {
    const words = text.split(' ');
    return words.slice(0, wordCount).join(' ') + (words.length > wordCount ? "..." : "");
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
    return diffInHours === 0 ? "Just now" : `${diffInHours} hours ago`;
  };


  const transformData = (data) => {
    if (!data) return [];
    return Object.values(data).map((article) => ({
      tag: article.subtopic || "General",
      title: article.title,
      description: getFirstWords(article.content, 30),
      text: article.content,
      time: formatTime(article.date),
      topic: article.topic,
      id: article.id
    }));
  };

  const newsData = flaskData ? transformData(flaskData) : [];

  // Handle article click to navigate to the detailed view
  const handleArticleClick = (article) => {
    navigate('/article', { state: { article } });
  };

  return (
    <div className="search">
      {/* Search Form */}
      <form onSubmit={searchArticles} className="search-bar-container">
        <input
          type="text"
          placeholder="Search articles..."
          value={searchQuery}
          onChange={handleSearchChange}
          className="search-input"
        />
        <button type="submit" className="search-button">Search</button>
      </form>

      {/* Loading and Error Messages */}
      {loading && <p>Loading search results...</p>}
      {error && <p>Error: {error}</p>}

      {/* Search Results */}
      <section className="news-section">
        <h3 className="sub-header">Search Results</h3>
        <div className="news-list">
          {newsData.length > 0 ? (
            newsData.map((news, index) => (
              <div
                key={index}
                onClick={() => handleArticleClick(news)}
                className="news-item"
              >
                <div className="section-tag">{news.tag}</div>
                <div className="internal-header">{news.title}</div>
                <div className="internal-description">{news.description}</div>
              </div>
            ))
          ) : (
            !loading && <p>No articles found matching your search.</p>
          )}
        </div>
      </section>
    </div>
  );
};

export default Search;
