import React, { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults([]);

    if (!url || !query) {
      setError("Please enter both URL and search query.");
      setLoading(false);
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/search/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, query }),
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(`Network response not ok: ${response.status} ${text}`);
      }

      const data = await response.json();

      if (data.error) {
        setError(data.error);
        setResults([]);
      } else {
        // Each result should now include HTML DOM content as 'html_chunk'
        setResults(data.results || []);
      }
    } catch (err) {
      console.error("Fetch error:", err);
      setError(
        `Error fetching results. Make sure backend is running and URL is correct.\nDetails: ${err.message}`
      );
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1 style={{ color: "#1a237e" }}>Website Content Search</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
        <div style={{ marginBottom: "1rem" }}>
          <label style={{ marginRight: "0.5rem" }}>Website URL:</label>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="https://example.com"
            style={{
              width: "300px",
              padding: "0.5rem",
              borderRadius: "4px",
              border: "1px solid #ccc",
            }}
            required
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label style={{ marginRight: "0.5rem" }}>Search Query:</label>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter search text"
            style={{
              width: "300px",
              padding: "0.5rem",
              borderRadius: "4px",
              border: "1px solid #ccc",
            }}
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            backgroundColor: "#1976d2",
            color: "white",
            padding: "0.6rem 1.2rem",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
            transition: "background-color 0.3s",
          }}
          onMouseOver={(e) => (e.target.style.backgroundColor = "#0d47a1")}
          onMouseOut={(e) => (e.target.style.backgroundColor = "#1976d2")}
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {error && <p style={{ color: "red", whiteSpace: "pre-wrap" }}>{error}</p>}

      <h2 style={{ color: "#1a237e" }}>Search Results:</h2>
      {results.length === 0 && !loading ? (
        <p>No results yet</p>
      ) : (
        results.map((chunk, index) => (
          <div
            key={index}
            style={{
              border: "1px solid #ccc",
              padding: "1rem",
              marginBottom: "1rem",
              borderRadius: "8px",
              backgroundColor: "#f9f9f9",
              boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
              whiteSpace: "pre-wrap",
            }}
          >
            <p>
              <strong>Rank:</strong> {chunk.rank}
            </p>
            <p>
              <strong>Content:</strong> {chunk.content}
            </p>
            <p style={{ color: "green" }}>
              <strong>Relevance:</strong>{" "}
              {chunk.relevance_score
                ? `${(chunk.relevance_score * 100).toFixed(1)}% match`
                : "N/A"}
            </p>
            <p style={{ color: "green" }}>
              <strong>Tokens:</strong> {chunk.token_count}
            </p>
            {chunk.html_chunk && (
              <div
                style={{
                  marginTop: "0.5rem",
                  padding: "0.5rem",
                  border: "1px dashed #1976d2",
                  borderRadius: "4px",
                  backgroundColor: "#e3f2fd",
                }}
              >
                <strong>HTML DOM:</strong>
                <pre style={{ whiteSpace: "pre-wrap", fontSize: "0.85rem" }}>
                  {chunk.html_chunk}
                </pre>
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );
}

export default App;
