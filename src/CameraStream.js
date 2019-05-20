import React, { Component } from "react";
import "./style.css";
import novideo from "./novideo.jpg";
const domain = "localhost:5000";

class CameraStream extends Component {
  constructor(props) {
    super(props);
    this.state = {
      ip: "",
      src: novideo
    };
  }

  onClickGetVideo = () => {
    this.setState({
      src: "http://" + domain + "/video_feed?id=" + this.state.ip
    });
  };

  onClickStopVideo = () => {
    this.setState({
      src: novideo
    });
  };

  render() {
    return (
      <div>
        <div style={{ display: "inline-flex", margin: "45px 0px 10px 0px" }}>
          <p className="title-camera"> IP CAMERA: </p>
          <input
            className="tags-input"
            id="ip_input"
            type="text"
            name="fname"
            placeholder="192.168.0.1:8080"
            onChange={event => {
              this.setState({
                ip: event.target.value
              });
            }}
          />
        </div>
        <br />
        <button
          className="button-get-video"
          onClick={() => this.onClickGetVideo()}
        >
          Connect Video
        </button>
        <button
          className="button-stop-video"
          onClick={() => this.onClickStopVideo()}
        >
          Stop
        </button>
        <br />
        <br />
        <img
          heigh="400px"
          background="white"
          id="bg"
          src={this.state.src}
          alt="NoVideo"
        />
      </div>
    );
  }
}

export default CameraStream;
