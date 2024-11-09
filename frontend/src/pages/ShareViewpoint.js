import React, { useState } from 'react';
import TextBox from '../components/TextBox';
import './ShareViewpoint.css';

const ShareViewpoint = () => {
  const [headline, setHeadline] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = () => {
    if (headline && content) {
      alert('Your article has been submitted!');
      setHeadline('');
      setContent('');
    } else {
      alert('Please fill in both fields.');
    }
  };

  return (
    <div className="share-viewpoint-page">
      <h2>Share Your Viewpoint</h2>
      <TextBox
        headline={headline}
        setHeadline={setHeadline}
        content={content}
        setContent={setContent}
        handleSubmit={handleSubmit}
      />
    </div>
  );
};

export default ShareViewpoint;
