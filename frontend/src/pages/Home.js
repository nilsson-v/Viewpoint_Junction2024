import React, { useRef } from 'react';
import './Home.css';

const Home = () => {
  const newsData = [
    {
      tag: "Us economy",
      title: "Qatar asks Hamas leaders to leave after US pressure",
      description: "Warren Buffet has bought a new home in Chinatown and is looking for a nice wife...",
      image: "https://via.placeholder.com/150",
      time: "5 hours ago"
    },
    {
      tag: "Us economy",
      title: "Something really interesting has happened in US and BLA BLa",
      description: "Warren Buffet has bought a new home in Chinatown and is looking for a nice wife...",
      image: "https://via.placeholder.com/150",
      time: "5 hours ago"
    },
    {
      tag: "Us economy",
      title: "Something really interesting has happened in US and BLA BLa",
      description: "Warren Buffet has bought a new home in Chinatown and is looking for a nice wife...",
      image: "https://via.placeholder.com/150",
      time: "5 hours ago"
    },
    {
      tag: "Us economy",
      title: "Something really interesting has happened in US and BLA BLa",
      description: "Warren Buffet has bought a new home in Chinatown and is looking for a nice wife...",
      image: "https://via.placeholder.com/150",
      time: "5 hours ago"
    },
  ];

  const worldRef = useRef(null);
  const internalRef = useRef(null);
  const usRef = useRef(null);

  const scrollToSection = (ref) => {
    window.scrollTo({
      top: ref.current.offsetTop - 100,
      behavior: 'smooth'
    });
  };

  return (
    <div className="home">
      {/* Section Links at the top-right */}
      <div className="section-links">
        <span onClick={() => scrollToSection(worldRef)}>World</span>
        <span onClick={() => scrollToSection(internalRef)}>Internal Affairs</span>
        <span onClick={() => scrollToSection(usRef)}>United States</span>
      </div>

      <h2 className="section-title">Happening Now</h2>

      {/* World Section */}
      <section ref={worldRef} className="news-section">
        <h3 className="sub-header">World</h3>
        <div className="news-grid">
          {newsData.map((news, index) => (
            <div key={index} className="news-card">
              <div className="tag">{news.tag}</div>
              <h4 className="news-title">{news.title}</h4>
              <p className="news-description">{news.description}</p>
              <img src={news.image} alt={news.title} className="news-image" />
              <p className="news-time">{news.time}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Internal Affairs Section */}
      <section ref={internalRef} className="news-section">
        <h3 className="sub-header">Internal Affairs</h3>
        <div className="news-list">
          <div className="news-item">
            <span className="tag">Finnish Parliament Drama - 1 day ago</span>
            <h4>Sanna Marin has bought a new car...</h4>
            <p>Details of internal affairs...</p>
          </div>
        </div>
      </section>

      {/* United States Section */}
      <section ref={usRef} className="news-section">
        <h3 className="sub-header">United States</h3>
        <div className="news-list">
          <div className="news-item">
            <span className="tag">US News - 2 hours ago</span>
            <h4>Breaking news in the US...</h4>
            <p>Updates on current events in the United States...</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
