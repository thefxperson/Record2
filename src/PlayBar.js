import './PlayBar.css';
import React from 'react'

class PlayBar extends React.Component{
  constructor(props){
    super(props);
    this.state = {currTime: 0,
                  barStyle: { width: 0}}

    this.renderBar = this.renderBar.bind(this);
    this.tick = this.tick.bind(this);
  }

  // start of lifecycle
  componentDidMount() {
    // set timer to update bar every 1sec
    if(this.props.maxTime > 0){
      this.timer = setInterval(
        () => this.tick(),
        1000
      );
    }

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
    if(this.props.song != prevProps.song) {
      clearInterval(this.timer);
      this.setState({
        currTime: 0
      })

      // restart timer
      this.timer = setInterval(
        () => this.tick(),
        1000
      );
    }
  }

  // update playbar every 1 sec
  tick() {
    this.setState({
      currTime: this.state.currTime+1
    })

    // update in separate function
    this.renderBar();

    // make sure it stops when time is equal to max
    if(this.state.currTime == this.state.maxTime) {
      clearInterval(this.timer);
    }
  }

  // separate function from tick so we can update on window size adjust
  renderBar() {
    var new_max = document.getElementsByClassName("PctBar")[0].offsetWidth
    this.setState({
      barStyle: { width: (this.state.currTime / this.props.maxTime) * new_max}
    })
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
        <p>{this.formatTime(this.state.currTime)}</p>
        <div className="PctBar">
          <div className="ProgressBar" style={this.state.barStyle}></div>
        </div>
        <p>{this.formatTime(this.props.maxTime)}</p>
      </div>
    );
  }
}

export default PlayBar;
