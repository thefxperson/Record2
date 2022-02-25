import './PlayBar.css';
import React from 'react'

class PlayBar extends React.Component{
  constructor(props){
    super(props);
  }

  render(){
    return (
      <div className="PlayBar">
        <p>{this.props.currTime}</p>
        <div className="PctBar">
          <div className="ProgressBar"></div>
        </div>
        <p>{this.props.maxTime}</p>
      </div>
    );
  }
}

export default PlayBar;
