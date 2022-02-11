import './NowPlaying.css';
import React from 'react'
import placeholder from "./placeholder.png"
const {ipcRenderer} = window.require("electron")

class NowPlaying extends React.Component{
  constructor(props){
    super(props);
    // default state
    this.state = {
      art: placeholder,
      song: "Play a song to scrobble...",
      artist: "..."
    }

    //bind event listener to class
    this.updateSong = this.updateSong.bind(this);
  }

  componentDidMount(){
    // add event listener
    ipcRenderer.on("newSong", (event, args) => {
      console.log(args)
      this.updateSong(args)
    })
  }

  updateSong(e){
    this.setState({
      art: e.newArt,
      song: e.newSong,
      artist: e.newArtist
    })
  }

  render(){
    return (
      <div className="NowPlaying">
          <img src={this.state.art} className="NowPlaying-art" alt="album-art" />
          <h3>{this.state.song}</h3>
          <h4>{this.state.artist}</h4>
      </div>
    );
  }
}

export default NowPlaying;
