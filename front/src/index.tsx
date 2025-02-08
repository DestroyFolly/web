import React from 'react';
import ReactDOM from 'react-dom/client'; // Используем ReactDOM из client
import App from './App'; // Убедись, что путь корректный

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
