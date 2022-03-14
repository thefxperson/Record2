import './FileInput.css';
import React from 'react'
const {ipcRenderer} = window.require("electron")

class FileInput extends React.Component{
  constructor(props){
    super(props);

    this.sendFilePath = this.sendFilePath.bind(this)
  }

  sendFilePath(){
    // send info to python
    console.log(this.path.value)
    ipcRenderer.send("scrobbleSong", {"fun": "scrobbleSong",
                                      "data": {"path": this.path.value}})
  }

  render(){
    return (
      <div className="FileInput">
          <p>
            <input type="text" placeholder="Path/To/Song.mp3" ref={(c) => this.path = c} />
            <button type="button" onClick={this.sendFilePath}>Scrobble</button>
          </p>
      </div>
    );
  }
}

export default FileInput;
