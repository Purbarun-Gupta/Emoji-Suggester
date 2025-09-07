import React, { useState } from "react";
import "./App.css"; // Custom styles

function App() {
  const [input, setInput] = useState("");
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setPredictions([]);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        // When deployed, replace with:
        // "https://emoji-suggester-backend.onrender.com/predict"
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      });

      if (!response.ok) {
        throw new Error("Failed to fetch predictions");
      }

      const data = await response.json();
      setPredictions(data.predictions || []);
    } catch (err) {
      setError("⚠️ Error fetching predictions. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Navbar */}
      <header className="navbar">
        <span className="logo">🔶 Emoji Suggester</span>
      </header>

      {/* Hero Section */}
      <main className="main">
        <h1 className="headline">
          Suggest the perfect emoji for <br /> your text
        </h1>
        <p className="subtext">
          Just type and get instant emoji recommendations.
        </p>

        {/* Input Form */}
        <form onSubmit={handleSubmit} className="form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter your text here..."
            className="input"
          />
          <button type="submit" className="btn">
            Get Emojis
          </button>
        </form>

        {/* Status Messages */}
        {loading && <p className="loading">⏳ Loading...</p>}
        {error && <p className="error">{error}</p>}

        {/* Predictions */}
        <section className="results">
          {predictions.length > 0 && <h3>Top Emoji Suggestions</h3>}
          <div className="emoji-cards">
            {predictions.map((p, index) => (
              <div key={index} className="emoji-card">
                <span className="emoji">{p.emoji}</span>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
