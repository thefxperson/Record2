import './MicScrobble.css';
import React from 'react'
const {ipcRenderer} = window.require("electron")

class MicScrobble extends React.Component{
  constructor(props){
    super(props);
    this.scrobble = this.scrobble.bind(this)
  }

  scrobble(){
    // send info to python
    ipcRenderer.send("scrobbleSong", {"fun": "scrobbleMic"})
  }

  render(){
    return (
      <div className="MicScrobble">
          <button type="button" onClick={this.scrobble}>Scrobble from Mic</button>
      </div>
    );
  }
}

export default MicScrobble;
