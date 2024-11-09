import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <div className="navbar-container">
        <div className='title-container'>
          <h1 className="title">Viewpoint</h1>
        </div>
      <nav className="all-links-container">
        <div className="other-links-container">
          <div className=''>
            <Link to="/search" className="nav-item">Search</Link>
            <Link to="/" className="nav-item">Happening Now</Link>
            <Link to="/topics" className="nav-item">Topics</Link>
          </div>
        </div>
        <div className="viewpoint-link-container">
          <Link to="/share" className="viewpoint">Share Your Viewpoint</Link>
        </div>
      </nav>
    </div>
  );
};

export default Navbar;