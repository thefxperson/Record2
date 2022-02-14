import './NowPlaying.css';
import React from 'react'
const {ipcRenderer} = window.require("electron")

class NowPlaying extends React.Component{
  constructor(props){
    super(props);
    // default state
    this.state = {
      art: "None",
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
    // only render if song returns proper art
    let album_art;
    if(this.state.art === "None"){
      // default art
      album_art =
      <div className="NowPlaying-BlankArt">
          <div className="NowPlaying-Square"></div>
          <div className="NowPlaying-Circle1"></div>
          <div className="NowPlaying-Circle2"></div>
          <div className="NowPlaying-Circle3"></div>
          <div className="NowPlaying-Circle4"></div>
      </div>
    }else{
      album_art = <img src={this.state.art} className="NowPlaying-art" alt="album-art" />
    }


    return (
      <div className="NowPlaying">
          {album_art}
          <h3>{this.state.song}</h3>
          <h4>{this.state.artist}</h4>
      </div>
    );
  }
}

export default NowPlaying;
