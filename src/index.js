import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <React.StrictMode>
    <App song="Devil in a New Dress" artist="Kanye West" art="https://lastfm.freetls.fastly.net/i/u/770x0/8a071c4b073625018de5f0ac58727511.jpg#8a071c4b073625018de5f0ac58727511" />
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
