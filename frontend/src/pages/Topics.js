import React from 'react';
import './Topics.css';

const Topics = () => {
  return (
    <div className="topics-page">
      <h2>Popular Topics</h2>
      <div className="topics-grid">
        <div className="topic-card">Popular Topics</div>
        <div className="topic-card">Personal Viewpoints</div>
        <div className="topic-card">All Topics</div>
      </div>
    </div>
  );
};

export default Topics;
