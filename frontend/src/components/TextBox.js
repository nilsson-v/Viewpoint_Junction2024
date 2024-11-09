import React from 'react';
import './TextBox.css';

const TextBox = ({ headline, setHeadline, content, setContent, handleSubmit }) => {

  // Modified handleSubmit to include the timestamp and create the desired JSON structure
  const handleFormSubmit = async (e) => {
    e.preventDefault();

    // Get the current timestamp
    const timestamp = new Date().toISOString();

    // Create the JSON structure
    const jsonData = {
      data: {
        "1": { // Assuming '1' is a placeholder for unique id
          title: headline,
          date: timestamp,
          content: content,
          source: "User viewpoint"
        }
      }
    };

    console.log("Generated JSON:", jsonData); // Log the JSON data to check the structure

    // Send a POST request with the JSON data to the Flask API
    try {
      const response = await fetch('https://flaskapi-529120302078.europe-north1.run.app/process_user_viewpoint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json', // Set content type to application/json
        },
        body: JSON.stringify(jsonData) // Convert the JSON data to a string
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log("Response from Flask API:", data); // Log the response from the server

      // Call the provided handleSubmit function, passing the generated JSON
      handleSubmit(jsonData);

    } catch (error) {
      console.error('Error sending data:', error); // Log any error that occurs during the fetch
    } finally {
      // Clear the input fields after submitting (optional)
      setHeadline("");
      setContent("");
    }
  };

  return (
    <form onSubmit={handleFormSubmit} className="text-box-form">
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
