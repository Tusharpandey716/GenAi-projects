import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [orderId, setOrderId] = useState("");
  const [orderDetails, setOrderDetails] = useState("");
  const [query, setQuery] = useState("");
  const [aiResponse, setAiResponse] = useState("");

  // Fetch Shipment Details
  const trackShipment = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/track", { order_id: orderId });
      setOrderDetails(response.data.details);
    } catch (error) {
      setOrderDetails("Order not found");
    }
  };

  // Ask AI Assistant
  const askAI = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/ask", { query });
      setAiResponse(response.data.response);
    } catch (error) {
      setAiResponse("Error getting response");
    }
  };

  return (
    <div className="container">
      {/* Shipment Tracking Section */}
      <div className="section tracking">
        <h1>Track Your Shipment</h1>
        <input type="text" value={orderId} onChange={(e) => setOrderId(e.target.value)} placeholder="Enter Order ID" />
        <button onClick={trackShipment}>Track</button>
        <p><strong>Status:</strong> {orderDetails}</p>
      </div>

      {/* AI Assistant Section */}
      <div className="section assistant">
        <h1>Ask AI Assistant</h1>
        <input type="text" value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Ask a question" />
        <button onClick={askAI}>Ask</button>
        <p><strong>AI Response:</strong> {aiResponse}</p>
      </div>
    </div>
  );
}

export default App;
