import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Article.css';

const ArticleDetail = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { article } = location.state || {};

  // Embed the Polis script when the component loads
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://pol.is/embed.js';
    script.async = true;
    document.body.appendChild(script);
    return () => {
      document.body.removeChild(script);
    };
  }, []);

  if (!article) return <p>No article found</p>;

  return (
    <div className="article-detail">
      <button className="back-button" onClick={() => navigate(-1)}>← Back</button>
      <div className="content-container">
        {/* Article Content */}
        <div className="article-content">
          <h2>{article.title}</h2>
          <p>{article.content}</p>
        </div>

        {/* Placeholder Section with Polis Embed */}
        <div className="placeholder">
          <div className='polis' data-conversation_id='6kt4a4fxmn'></div>
        </div>
      </div>
    </div>
  );
};

export default ArticleDetail;
