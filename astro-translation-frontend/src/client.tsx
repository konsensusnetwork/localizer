import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './components/App';

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', () => {
  // Mount the main app
  const appElement = document.getElementById('app-root');
  if (appElement) {
    const root = ReactDOM.createRoot(appElement);
    root.render(<App />);
  }
});