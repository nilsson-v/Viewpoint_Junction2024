import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <header className="navbar">
      <h1 className="title">Viewpoint</h1>
      <nav className="nav-links">
        <Link to="/" className="nav-item">Happening Now</Link>
        <Link to="/topics" className="nav-item">Topics</Link>
        <Link to="/share" className="nav-item">Share Your Viewpoint</Link>
        <Link to="/search" className="nav-item">Search</Link>
      </nav>
    </header>
  );
};

export default Navbar;
