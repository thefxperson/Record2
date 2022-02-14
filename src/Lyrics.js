import './Lyrics.css';
import React from 'react'

class Lyrics extends React.Component{
  constructor(props){
    super(props);

    this.showLyrics = this.showLyrics.bind(this)
    this.state = {
      showLyrics: false
    }
  }

  showLyrics() {
    this.setState({showLyrics: !this.state.showLyrics})
  }

  render(){
    let lyricsPane
    if (this.state.showLyrics === true){
      lyricsPane =
      <div className="LyricsPane">
        <h3>Lyrics</h3>
        <div className="LyricsVerse">
          <p>Lorem ipsum dolor sit amet,</p>
          <p>consectetur adipiscing elit.</p>
          <p>Maecenas euismod,</p>
          <p>lacus eleifend vulputate egestas</p>
        </div>
        <div className="LyricsVerse">
          <p>massa justo auctor sem,</p>
          <p>a tincidunt ex lectus in quam.</p>
          <p>Donec euismod placerat sem sed porttitor.</p>
          <p>Morbi dolor velit,</p>
        </div>
      </div>
    }
    return (
      <div className="Lyrics">
        {lyricsPane}
        <button type="button" onClick={this.showLyrics}>Lyrics</button>
      </div>
    );
  }
}

export default Lyrics;
