import React from 'react';
import './home.css';

const Home = () => {
  const newsData = [
    {
      tag: "Us economy",
      title: "Something really interesting has happened in US and BLA BLa",
      description: "Warren Buffet has bought a new home in Chinatown and is looking for a nice wife...",
      image: "https://via.placeholder.com/150"
    },
    {
      tag: "Us economy",
      title: "Something really interesting has happened in US and BLA BLa",
      description: "Warren Buffet has bought a new home in Chinatown and is looking for a nice wife...",
      image: "https://via.placeholder.com/150"
    },
    {
      tag: "Us economy",
      title: "Something really interesting has happened in US and BLA BLa",
      description: "Warren Buffet has bought a new home in Chinatown and is looking for a nice wife...",
      image: "https://via.placeholder.com/150"
    }
  ];

  return (
    <div className="home">
      <h2 className="section-title">Happening Now</h2>
      <div className="news-grid">
        {newsData.map((news, index) => (
          <div key={index} className="news-card">
            <div className="tag">{news.tag}</div>
            <h3 className="news-title">{news.title}</h3>
            <p className="news-description">{news.description}</p>
            <img src={news.image} alt={news.title} className="news-image" />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
