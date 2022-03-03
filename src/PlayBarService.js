import './PlayBar.css';
import React from 'react'

class PlayBarService extends React.Component{
  constructor(props){
    super(props);
    this.state = {currTime: 0,
                  barStyle: { width: 0}}

    this.renderBar = this.renderBar.bind(this);
  }

  // start of lifecycle
  componentDidMount() {

    // re-render bar width on resize
    window.addEventListener('resize', this.renderBar);
  }

  // end of lifecycle
  componentWillUnmount() {
    clearInterval(this.timer);
    window.removeEventListener('resize', this.renderBar);
  }

  // reset timer on new song
  componentDidUpdate(prevProps) {
    // check to make sure new song
    if(this.props.currPerc != prevProps.currPerc) {
      this.renderBar()
    }
  }

  // separate function from tick so we can update on window size adjust
  renderBar() {
    var new_max = document.getElementsByClassName("PctBar")[0].offsetWidth
    console.log(new_max)
    this.setState({
      barStyle: { width: this.props.currPerc * new_max}
    })
    console.log(this.props.currPerc * new_max)
  }

  formatTime(secs) {
    var min = Math.floor(secs / 60);
    var rem = secs % 60;
    if(rem < 10){
      rem = '0' + String(rem)   // prob bad style to double cast but idgaf
    }
    return String(min) + ':' + String(rem)
  }

  render(){
    return (
      <div className="PlayBar">
        <p>{this.formatTime(this.props.currTime)}</p>
        <div className="PctBar">
          <div className="ProgressBar" style={this.state.barStyle}></div>
        </div>
        <p>{this.formatTime(this.props.maxTime)}</p>
      </div>
    );
  }
}

export default PlayBarService;
