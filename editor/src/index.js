import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';  // Assuming your styles are in index.css
import App from './App';  // Main App component
import reportWebVitals from './reportWebVitals';  // For performance measurement

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')  // Mounts React app to the DOM element with ID 'root'
);

// Measure performance in your app, pass a function (for example: reportWebVitals(console.log))
// or send to an analytics endpoint.
reportWebVitals(console.log);  // Logs performance metrics
