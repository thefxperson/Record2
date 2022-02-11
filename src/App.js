import logo from './logo.svg';
import './App.css';
import React from 'react'

class App extends React.Component{
  constructor(props){
    super(props);
  }

  render(){
    return (
      <div className="App">
        <header className="App-header">
          <img src={this.props.art} className="App-art" alt="album-art" />
          <p>{this.props.song} - {this.props.artist}</p>
        </header>
      </div>
    );
  }
}
/*function App(props){
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="album-art" />
        <p>{props.song} - {props.artist}</p>
      </header>
    </div>
  );
}*/

export default App;
