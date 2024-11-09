import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Article.css';

const ArticleDetail = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Access the article from location.state
  const { article } = location.state || {};

  // Debugging: Log the article to ensure it's correctly passed
  console.log("Article received in ArticleDetail:", article);

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

  // If no article is passed, show a fallback message
  if (!article) {
    return <p>No article found</p>;
  }

  return (
    <div className="article-detail">
      {/* Back Button */}
      <button className="back-button" onClick={() => navigate(-1)}>← Back</button>
      <div className="text-container">
        {/* Article Content */}
        <div className="article-text">
          <h2>{article.title}</h2>
          <p>{article.text}</p> 
        </div>
        <div
          className="polis"
          data-conversation_id="6kt4a4fxmn"
        ></div>
      </div>
    </div>
  );
}
export default ArticleDetail;
