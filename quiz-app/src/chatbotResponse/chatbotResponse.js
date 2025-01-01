import React, { useState } from "react";
import InputBox from "../inputBox/inputBox";

// Chatbot Response Component - Fetches chatbot response from the backend and displays user/bot interaction
const ChatbotResponse = () => {
  const [messages, setMessages] = useState([]);

  const addMessage = async (message) => {
    // Add user message to the chat
    const userMessage = { text: message, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // Fetch chatbot response from the backend
    try {
      const response = await fetch("http://localhost:8080/quiz", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: message }),
      });

      const data = await response.json();

      // Add chatbot message to the chat
      const botMessage = { text: data.response, sender: "bot" };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Error fetching chatbot response:", error);
    }
  };

  return (
    <div className="chatbox">
      <div className="response">
        {messages.map((message, index) => (

          // Display the messages in the chat based on the sender (user or bot)
            <p key={index} className={`message ${message.sender === "user" ? "user" : "bot"}`} style={{ paddingTop: "10px" }}>
            <strong style={{ color: message.sender === "bot" ? "#bf0228" : "black" }}>
              {message.sender === "user" ? "You: " : "QuizBot: "}
            </strong> 
            {message.sender === "bot" ? (
              // Display answer choices as list
              message.text.split('\n').map((line, i) => (
                <span key={i}>{line}<br /></span>))) : (message.text)}
          </p>
        ))}
      </div>
      <InputBox onSend={addMessage} />
    </div>
  );
};

export default ChatbotResponse;
