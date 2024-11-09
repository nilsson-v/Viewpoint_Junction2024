import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Article.css';

const ArticleDetail = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Access the article or opinion from location.state
  const { article, opinion } = location.state || {};

  // State to store the conversation ID
  const [conversationId, setConversationId] = useState('');

  // Function to generate a conversation ID
  const generateConversationId = (id, isOpinion = false) => {
    if (!id) return null;
    // For opinions: Use the first 10 characters of the ID
    if (isOpinion) {
      return id.slice(0, 10);
    }
    // For articles: Pad the article ID with "AA" until it's 10 characters long
    return id.padEnd(10, 'AA').slice(0, 10);
  };

  // Determine if we are displaying an article or an opinion
  const content = article || opinion;
  const isOpinion = !!opinion;

  // Set the conversation ID based on the content ID
  useEffect(() => {
    if (!content || !content.id) {
      console.error("Content or content ID is missing");
      return;
    }

    // Generate the conversation ID using the content ID
    const conversationId = generateConversationId(content.id, isOpinion);
    setConversationId(conversationId);
    console.log("Generated conversation ID:", conversationId);
  }, [content, isOpinion]);

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

  // If no content is passed, show a fallback message
  if (!content) {
    return <p>No content found</p>;
  }

  return (
    <div className="article-detail">
      {/* Back Button */}
      <button className="back-button" onClick={() => navigate(-1)}>← Back</button>
      <div className="text-container">
        {/* Content (Article or Opinion) */}
        <div className="article-text">
          <h2>{content.title}</h2>
          <p>{content.text || content.description}</p>
        </div>
        {/* Embed the Polis conversation */}
        {conversationId && (
          <div
            className="polis"
            data-page_id={conversationId}
            data-site_id="polis_site_id_RQwrz6mTCTd6yrfTDA"
            show_vis="true"
            auth_needed_to_vote="false"
            auth_needed_to_write="false"
            ucsd="false"
            auth_opt_fb="false"
            auth_opt_tw="false"
          ></div>
        )}
      </div>
    </div>
  );
};

export default ArticleDetail;
