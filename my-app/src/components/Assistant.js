import React, { useState } from "react";
import "./Assistant.css";

const Assistant = () => {
  const [messages, setMessages] = useState([
    { type: "bot", text: "Hello! How can I assist you today?" },
  ]);

  const handleMicrophoneClick = () => {
    // Simulate user voice input and bot response
    setMessages((prev) => [
      ...prev,
      { type: "user", text: "Listening..." },
      { type: "bot", text: "I heard you! Let me process that." },
    ]);
  };

  return (
    <div className="assistant-container">
      {/* Chat window */}
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.type === "bot" ? "bot" : "user"}`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      {/* Microphone button */}
      <div className="mic-container">
        <button onClick={handleMicrophoneClick} className="mic-button">
          <i className="material-icons">mic</i>
        </button>
      </div>
    </div>
  );
};

export default Assistant;
