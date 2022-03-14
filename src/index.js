import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import NowPlaying from './NowPlaying';
import FileInput from './FileInput';
import MicScrobble from './MicScrobble';
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <div>
    <NowPlaying />
    <FileInput />
    <MicScrobble />
  </div>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
