import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<{ title: string; price: string; url: string }[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const response = await fetch(`http://127.0.0.1:5000/?query=${encodeURIComponent(query)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (!response.ok) {
        throw new Error('Failed to fetch search results');
      }
      const data: { results: { title: string; price: string; url: string }[] } = await response.json();
      setResults(data.results || []);
    } catch (err) {
      setError((err as Error).message);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>eBay Scanner</h1>
      </header>

      <main className="main">
        <form className="search-form" onSubmit={handleSearch}>
          <input
            type="text"
            className="search-input"
            placeholder="Search for items"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button className="search-button" type="submit">Search</button>
        </form>

        {error && <p className="error-message">{error}</p>}

        <ul className="results-list">
          {results.map((item, index) => (
            <li key={index} className="result-item">
              <a href={item.url} target="_blank" rel="noopener noreferrer">
                {item.title} - {item.price}
              </a>
            </li>
          ))}
        </ul>
      </main>
    </div>
  );
}

export default App;
