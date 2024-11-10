import React, { useEffect, useState, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Article.css';

const ArticleDetail = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Access the article or opinion from location.state
  const { article, opinion } = location.state || {};

  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');

  // Ref to access the textarea
  const textareaRef = useRef(null);

  // Function to adjust the height of the textarea automatically
  const handleInputChange = (e) => {
    setQuestion(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'; // Reset height
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`; // Set height based on content
    }
  };

  const handleQuestionSubmit = async (e) => {
    e.preventDefault();
    if (question.trim() === '') return;
  
    try {
      // Prepare the data to be sent in the request
      const payload = {
        content: article?.text || opinion?.text || '',
        question: question,
      };
  
      // Send a POST request to the specified endpoint
      const response = await fetch('https://flaskapi-529120302078.europe-north1.run.app/ask_question', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
  
      // Parse the JSON response
      const data = await response.json();
  
      if (response.ok) {
        // Display the server response in the response box
        setResponse(data.response || 'No answer provided.');
      } else {
        // Handle any error responses
        setResponse('Error: Could not get a response. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting question:', error);
      setResponse('An error occurred. Please try again later.');
    }
  
    // Clear the question input field after submission
    setQuestion('');
  };
  

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
    <button className="back-button" onClick={() => navigate(-1)}>← Back</button>
    <div className="content-container">
      <div className="article-text">
        <div className='text-container'>
          <h2 className='header-text'>{article.title}</h2>
          <p className='article-info'>{article.text}</p>
        </div>

        {/* Answer Container at the bottom */}
        <div className="answer-container">
          <form onSubmit={handleQuestionSubmit}>
            <textarea
              ref={textareaRef}
              className="question-input"
              value={question}
              onChange={handleInputChange}
              placeholder="Ask for additional information..."
              rows="1"
            />
            <button type="submit" className="submit-button">Submit Question</button>
          </form>

          {response && (
            <div className="response-box">
              <p>{response}</p>
            </div>
          )}
        </div>
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
