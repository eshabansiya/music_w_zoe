import React, { useState } from 'react';
import './App.css';

function App() {
  const [song, setSong] = useState('');
  const [artist, setArtist] = useState('');
  const [accuracy, setAccuracy] = useState(null);
  const [reccomendations, setReccomendations] = useState(null);
  const [report, setReport] = useState(null);

  const handleClassify = () => {
    // You could pass song and artist to your backend here
    // For now, just fetch as before
    fetch("http://127.0.0.1:5000/api/classify")
      .then(res => res.json())
      .then(data => {
        setAccuracy(data.accuracy);
        setReport(data.report);
      })
      .catch(err => console.error(err));
  };

  const handleNearest = () => {
    // You could pass song and artist to your backend here
    // For now, just fetch as before
    fetch("http://127.0.0.1:5000/api/nearest")
      .then(res => res.json())
      .then(data => {
        setReccomendations(data.songs);
      })
      .catch(err => console.error(err));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h2>KNN Music Genre Classifier</h2>

        <div className="input-container">
          <input
            type="text"
            placeholder="Song Name"
            value={song}
            onChange={(e) => setSong(e.target.value)}
          />
          <input
            type="text"
            placeholder="Artist Name"
            value={artist}
            onChange={(e) => setArtist(e.target.value)}
          />
          <button onClick={handleClassify}>Classify Genre</button>
          <button onClick={handleNearest}>Nearest Songs</button>
        </div>

        {accuracy !== null ? (
          <div className="results">
            <p><strong>Accuracy:</strong> {reccomendations}</p>
          </div>
        ) : (
          <p>Enter a song and artist to be reccomended five songs!</p>
        )}
      </header>
    </div>
  );
}

export default App;
