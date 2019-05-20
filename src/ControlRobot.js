import React, { Component } from "react";
import { Button, InputNumber, Input, Row, Col } from "antd";
import request from "./config";
const preUrl = "";
const { TextArea } = Input;

class ControlRobot extends Component {
  constructor(props) {
    super(props);
    this.state = {
      x: 0,
      y: 0,
      x_goal: 0,
      y_goal: 0,
      direction: "",
      map: "",
      manual: false
    };
  }

  onXChange = event => {
    this.setState({
      x: event
    });
  };

  onYChange = event => {
    this.setState({
      y: event
    });
  };

  onXGoalChange = event => {
    this.setState({
      x_goal: event
    });
  };

  onYGoalChange = event => {
    this.setState({
      y_goal: event
    });
  };

  onDirectionChange = event => {
    this.setState({
      direction: event.target.value
    });
  };

  onManual = async () => {
    const manual = await request.axios.post(`${preUrl}/api/auto`, {
      message: "button"
    });

    this.setState({
      manual: true
    });
  };

  onAuto = async () => {
    const auto = await request.axios.post(`${preUrl}/api/auto`, {
      message: "auto"
    });
    this.setState({
      manual: false
    });
  };

  onInitialPosition = async () => {
    const auto = await request.axios.post(`${preUrl}/api/create`, {
      x: this.state.x,
      y: this.state.y,
      direction: this.state.direction,
      goal_x: this.state.x_goal,
      goal_y: this.state.y_goal
    });
  };

  onTurnRight = async () => {
    const right = await request.axios.post(`${preUrl}/api/direction`, {
      command: "east"
    });
  };

  onTurnLeft = async () => {
    const left = await request.axios.post(`${preUrl}/api/direction`, {
      command: "west"
    });
  };

  onGoStraight = async () => {
    const straight = await request.axios.post(`${preUrl}/api/direction`, {
      command: "north"
    });
  };

  onGoBack = async () => {
    const back = await request.axios.post(`${preUrl}/api/direction`, {
      command: "south"
    });
  };

  onPack = async () => {
    const back = await request.axios.post(`${preUrl}/api/direction`, {
      command: "pack"
    });
  };

  onMapChange = event => {
    this.setState({
      map: event.target.value
    });
  };

  onRequestMap = async () => {
    console.log("MAP HERE", this.state.map);
    const map = await request.axios.post(`${preUrl}/api/map`, {
      map: this.state.map
    });

    console.log(map);
  };

  render() {
    const { manual } = this.state;
    return (
      <div>
        <br />
        <br />
        <div>
          <div
            style={{
              width: "95%",
              margin: "auto",
              padding: "20px",
              border: "1px solid #c5c5c5",
              borderRadius: "15px"
            }}
          >
            <Row style={{ display: "flex" }}>
              <Col span={18}>
                <TextArea
                  placeholder="Initial map"
                  autosize={{ minRows: 4, maxRows: 4 }}
                  onChange={event => this.onMapChange(event)}
                />
              </Col>
              <Col span={6}>
                <Button
                  style={{ height: "100% !important" }}
                  type="primary"
                  onClick={() => this.onRequestMap()}
                >
                  Initital Map
                </Button>
              </Col>
            </Row>
          </div>

          <br />
          <br />

          <Row>
            <Col span={12}>
              <div
                className="d-pad"
                style={{
                  width: "90%",
                  margin: "auto",
                  padding: "20px",
                  border: "1px solid #c5c5c5",
                  borderRadius: "15px"
                }}
              >
                <Button type="primary" onClick={() => this.onAuto()}>
                  Auto Robot
                </Button>
                <br />
                <br />
                <Row>
                  <Col span={12}>
                    x{" "}
                    <InputNumber
                      min={0}
                      max={10}
                      step={1}
                      onChange={event => this.onXChange(event)}
                    />
                    <br />
                    <div style={{ height: "10px" }} />y{" "}
                    <InputNumber
                      min={0}
                      max={10}
                      step={1}
                      onChange={event => this.onYChange(event)}
                    />
                  </Col>
                  <Col span={12}>
                    goal_x{" "}
                    <InputNumber
                      min={0}
                      max={10}
                      step={1}
                      onChange={event => this.onXChange(event)}
                    />
                    <br />
                    <div style={{ height: "10px" }} />
                    goal_y{" "}
                    <InputNumber
                      min={0}
                      max={10}
                      step={1}
                      onChange={event => this.onXChange(event)}
                    />
                  </Col>
                </Row>

                <div style={{ height: "10px" }} />

                <Row style={{ display: "flex", padding: "0px 15px" }}>

                  direction <span style={{ marginRight: "5px" }}> </span>
                  <Input onChange={event => this.onDirectionChange(event)} />
                </Row>

                <br />

                <Button type="primary" onClick={() => this.onInitialPosition()}>
                  Initial Position
                </Button>
              </div>
            </Col>

            <Col span={12}>
              <div
                className="d-pad"
                style={{
                  width: "90%",
                  margin: "auto",
                  padding: "20px",
                  border: "1px solid #c5c5c5",
                  borderRadius: "15px"
                }}
              >
                <Button type="primary" onClick={() => this.onManual()}>
                  Manual Control
                </Button>
                <br />
                <br />

                <Row>
                  <Col span={8} />
                  <Col span={8}>
                    <Button
                      disabled={!manual}
                      onClick={() => this.onGoStraight()}
                    >
                      Go Straight
                    </Button>
                  </Col>
                  <Col span={8} />
                </Row>
                <Row>
                  <Col span={8}>
                    <Button
                      style={{ margin: "10px 0px" }}
                      disabled={!manual}
                      onClick={() => this.onTurnLeft()}
                    >
                      Turn Left
                    </Button>
                  </Col>
                  <Col span={8}>
                    <div style={{ padding: "10px" }}>
                      <Button
                        style={{
                          borderRadius: "50px"
                        }}
                        disabled={!manual}
                        onClick={() => this.onPack()}
                      >
                        Take
                      </Button>
                    </div>
                  </Col>
                  <Col span={8}>
                    <Button
                      style={{ margin: "10px 0px" }}
                      disabled={!manual}
                      onClick={() => this.onTurnRight()}
                    >
                      Turn Right
                    </Button>
                  </Col>
                </Row>
                <Row>
                  <Col span={8} />
                  <Col span={8}>
                    <Button disabled={!manual} onClick={() => this.onGoBack()}>
                      Go Back
                    </Button>
                  </Col>
                  <Col span={8} />
                </Row>
              </div>
            </Col>
          </Row>
        </div>
      </div>
    );
  }
}

export default ControlRobot;
