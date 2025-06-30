import React, { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [accuracy, setAccuracy] = useState(null);
  const [report, setReport] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/classify")
      .then(res => res.json())
      .then(data => {
        setAccuracy(data.accuracy);
        setReport(data.report);
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h2>KNN Music Genre Classifier</h2>
        {accuracy !== null ? (
          <div>
            <p><strong>Accuracy:</strong> {(accuracy * 100).toFixed(2)}%</p>
            <h3>Classification Report</h3>
            <pre>{JSON.stringify(report, null, 2)}</pre>
          </div>
        ) : (
          <p>Loading results...</p>
        )}
      </header>
    </div>
  );
}

export default App;
