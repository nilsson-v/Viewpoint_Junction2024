import React from 'react';
import './NewsCard.css';

const NewsCard = ({ title, description, image, tag }) => {
  return (
    <div className="news-card">
      <div className="tag">{tag}</div>
      <h3 className="news-title">{title}</h3>
      <p className="news-description">{description}</p>
      <img src={image} alt={title} className="news-image" />
    </div>
  );
};

export default NewsCard;
