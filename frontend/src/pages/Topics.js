import React, { useContext, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import { DataContext } from '../App'; // Import the context
import './topics.css';

const Topics = () => {
  // Access both flaskData (articles) and opinionsData from the DataContext
  const { flaskData, opinionsData, loading, error } = useContext(DataContext);

  const navigate = useNavigate(); // Initialize useNavigate
  const carouselRef = useRef(null);
  const opinionsRef = useRef(null);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [opinionsIndex, setOpinionsIndex] = useState(0);

  // Define the number of items to show at a time
  const itemsPerPage = 3;
  const totalItems = 6;
  const totalOpinions = 6;

  // Transform the data for topics
  const transformData = (data) => {
    if (!data) return [];
    return Object.values(data).map((item) => ({
      title: item.title,
      description: getFirstWords(item.content, 40),
      topic: item.topic,
      id: item.id, // Ensure each item has an ID
      text: item.content // Include the full content for the article page
    }));
  };

  // Helper function to get the first N words of a string
  const getFirstWords = (text, wordCount) => {
    const words = text.split(' ');
    return words.slice(0, wordCount).join(' ') + (words.length > wordCount ? "..." : "");
  };

  // Check if data is loading or if there's an error
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  // Transform the fetched data
  const topicsData = flaskData ? transformData(flaskData) : [];
  const opinionsTransformedData = opinionsData ? transformData(opinionsData) : [];

  // Handle article click to navigate to the Article page
  const handleArticleClick = (article) => {
    navigate('/article', { state: { article } });
  };

  // Functions for scrolling
  const scrollRight = (carouselRef, setIndex, index, totalItems) => {
    if (carouselRef.current) {
      const nextIndex = index + itemsPerPage;
      if (nextIndex < totalItems) {
        setIndex(nextIndex);
        carouselRef.current.scrollBy({ left: carouselRef.current.offsetWidth, behavior: 'smooth' });
      }
    }
  };

  const scrollLeft = (carouselRef, setIndex, index) => {
    if (carouselRef.current) {
      const prevIndex = index - itemsPerPage;
      if (prevIndex >= 0) {
        setIndex(prevIndex);
        carouselRef.current.scrollBy({ left: -carouselRef.current.offsetWidth, behavior: 'smooth' });
      }
    }
  };

  return (
    <div className="topics-page">
      {/* Topics Carousel */}
      <h2 className="site-header">Popular Topics</h2>
      <div className="carousel-container">
        {currentIndex > 0 && (
          <button className="arrow left-arrow" onClick={() => scrollLeft(carouselRef, setCurrentIndex, currentIndex)}>
            &#9664;
          </button>
        )}
        <div className="topics-grid" ref={carouselRef}>
          {topicsData.map((topic, index) => (
            <div
              key={index}
              className="topic-card"
              onClick={() => handleArticleClick(topic)} // Add onClick handler
            >
              <div className="topic-content">
                <h4 className="topic-title">{topic.title}</h4>
                <p className="topic-description">{topic.description}</p>
              </div>
            </div>
          ))}
        </div>
        {currentIndex + itemsPerPage < totalItems && (
          <button className="arrow right-arrow" onClick={() => scrollRight(carouselRef, setCurrentIndex, currentIndex, totalItems)}>
            &#9654;
          </button>
        )}
      </div>

      {/* Opinions Carousel */}
      <h2 className="site-header">Opinions</h2>
      <div className="carousel-container">
        {opinionsIndex > 0 && (
          <button className="arrow left-arrow" onClick={() => scrollLeft(opinionsRef, setOpinionsIndex, opinionsIndex)}>
            &#9664;
          </button>
        )}
        <div className="topics-grid" ref={opinionsRef}>
          {opinionsTransformedData.map((opinion, index) => (
            <div
              key={index}
              className="topic-card"
              onClick={() => handleArticleClick(opinion)} // Add onClick handler for opinions
            >
              <div className="topic-content">
                <h4 className="topic-title">{opinion.title}</h4>
                <p className="topic-description">{opinion.description}</p>
              </div>
            </div>
          ))}
        </div>
        {opinionsIndex + itemsPerPage < totalOpinions && (
          <button className="arrow right-arrow" onClick={() => scrollRight(opinionsRef, setOpinionsIndex, opinionsIndex, totalOpinions)}>
            &#9654;
          </button>
        )}
      </div>
    </div>
  );
};

export default Topics;
