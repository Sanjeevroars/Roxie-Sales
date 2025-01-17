import React, { useState } from 'react';
import './Chat.css';
import micIcon from './mic.png'; // Replace this with the path to your favicon image

const Chat = () => {
  const [messages, setMessages] = useState([]);

  const handleMicrophoneClick = () => {
    console.log("Microphone activated");
    // Add microphone activation logic here
  };

  return (
    <div className="chat-container">
      <div className="message-display">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.type === 'user' ? 'user' : 'assistant'}`}
          >
            {msg.text}
          </div>
        ))}
      </div>
      <div className="visualizer">Visualizer goes here</div>
      <div className="controls">
        <button onClick={handleMicrophoneClick}>
          <img src={micIcon} alt="Microphone" />
        </button>
      </div>
    </div>
  );
};

export default Chat;
