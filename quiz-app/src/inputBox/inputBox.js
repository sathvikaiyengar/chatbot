
import React, { useState } from "react";
import './inputBox.css';

// User Input Box Component
const InputBox = ({ onSend }) => {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim()) {
      onSend(input);
      setInput("");
    }
  };

  return (
    <div className="input-box">
    
      <input
        type="text"
        placeholder="Type your message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        // Additional capability to send message by pressing Enter key
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleSend();
          }
        }}
      />
      <button className="send-button" onClick={handleSend}>Send</button>
    </div>
  );
};

export default InputBox;