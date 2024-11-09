import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const [lastScrollY, setLastScrollY] = useState(window.scrollY);
  const [isVisible, setIsVisible] = useState(true);

  // Handle scroll to show/hide the navbar based on scroll direction
  const handleScroll = () => {
    const currentScrollY = window.scrollY;

    if (currentScrollY > lastScrollY) {
      // Scrolling down - hide navbar
      setIsVisible(false);
    } else {
      // Scrolling up - show navbar
      setIsVisible(true);
    }

    setLastScrollY(currentScrollY);
  };

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [lastScrollY]);

  return (
    <div className={`navbar-container ${isVisible ? 'show' : 'hide'}`}>
      <div className='title-container'>
        <h1 className="title">Viewpoint</h1>
      </div>
      <nav className="all-links-container">
        <div className="other-links-container">
          <NavLink 
            to="/search" 
            className="nav-item"
            activeClassName="active"
          >
            Search
          </NavLink>
          <NavLink 
            to="/" 
            exact 
            className="nav-item" 
            activeClassName="active"
          >
            Happening Now
          </NavLink>
          <NavLink 
            to="/topics" 
            className="nav-item" 
            activeClassName="active"
          >
            Topics
          </NavLink>
        </div>
        <div className="viewpoint-link-container">
          <NavLink 
            to="/share" 
            className="nav-item" 
            activeClassName="active"
          >
            Share Your Viewpoint
          </NavLink>
        </div>
      </nav>
    </div>
  );
};

export default Navbar;