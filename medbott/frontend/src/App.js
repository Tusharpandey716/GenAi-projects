import { useState } from "react";
import axios from "axios";
import { FaStethoscope, FaRobot } from "react-icons/fa";
import "./App.css";

function App() {
    const [question, setQuestion] = useState("");
    const [response, setResponse] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setResponse("");
        setLoading(true);

        try {
            const res = await axios.post("http://127.0.0.1:8000/query/", {
                question,
            });
            setResponse(res.data.response);
        } catch (error) {
            console.error("Error fetching response:", error);
            setResponse("⚠️ Error fetching data. Please try again.");
        }

        setLoading(false);
    };

    return (
        <div className="app-container">
            <div className="chat-container">
                <h1 className="chat-title">
                    <FaStethoscope className="icon" /> AI Medical Chatbot
                </h1>
                <form onSubmit={handleSubmit} className="chat-form">
                    <input
                        type="text"
                        className="chat-input"
                        placeholder="Enter disease name or symptoms..."
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        required
                    />
                    <button type="submit" className="chat-button">
                        <FaRobot className="bot-icon" /> Ask BioGPT
                    </button>
                </form>
                <div className="response-container">
                    {loading && <p className="loading">⏳ Fetching response...</p>}
                    {response && (
                        <div className="response-box">
                            <h3>Response:</h3>
                            <p>{response}</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default App;
