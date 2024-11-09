import React from 'react';
import './TextBox.css';

const TextBox = ({ headline, setHeadline, content, setContent, handleSubmit }) => {
  return (
    <form onSubmit={handleSubmit} className="text-box-form">
      <input
        type="text"
        placeholder="Headline..."
        value={headline}
        onChange={(e) => setHeadline(e.target.value)}
        className="headline-input"
      />
      <textarea
        placeholder="Express your viewpoint..."
        value={content}
        onChange={(e) => setContent(e.target.value)}
        className="content-textarea"
      />
      <button type="submit" className="send-button">Send</button>
    </form>
  );
};

export default TextBox;
