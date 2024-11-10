import React from 'react';
import './Loading.css';

const LoadingScreen = () => {
  return (
    <div className="loading-screen">
      <img src={`${process.env.PUBLIC_URL}/viewpoint.png`} alt="Loading Logo" className="loading-logo" />
      <p className="loading-text">Loading...</p>
      <p></p>
    </div>
  );
};

export default LoadingScreen;