import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Article.css';

const ArticleDetail = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Access the article from location.state
  const { article } = location.state || {};

  // State to store the conversation ID
  const [conversationId, setConversationId] = useState('');

  // Function to generate a padded conversation ID based on article.id
  const generateConversationId = (id) => {
    if (!id) return null;
    // Pad the article ID with "AA" until it's 10 characters long
    return id.padEnd(10, 'AA').slice(0, 10);
  };

  // Set the conversation ID based on the article ID
  useEffect(() => {
    if (!article || !article.id) {
      console.error("Article or article ID is missing");
      return;
    }

    // Generate the conversation ID using the article ID
    const conversationId = generateConversationId(article.id);
    setConversationId(conversationId);
    console.log("Generated conversation ID:", conversationId);
  }, [article]);

  // Embed the Polis script when the conversation ID is set
  useEffect(() => {
    if (!conversationId) return;

    const script = document.createElement('script');
    script.src = 'https://pol.is/embed.js';
    script.async = true;
    document.body.appendChild(script);

    return () => {
      if (script) {
        document.body.removeChild(script);
      }
    };
  }, [conversationId]);

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
        {/* Embed the Polis conversation */}
        {conversationId && (
          <div
            className="polis"
            data-page_id={conversationId}
            data-site_id="polis_site_id_RQwrz6mTCTd6yrfTDA"
          ></div>
        )}
      </div>
    </div>
  );
};

export default ArticleDetail;
