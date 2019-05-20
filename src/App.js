import React from "react";
import "./App.css";
import { Row, Col } from "antd";
import CameraStream from "./CameraStream";
import ControlRobot from "./ControlRobot";
import MapRobot from "./MapRobot";
import Header from "./Header";

function App() {
  return (
    <div className="App">
      <Header />
      <Row>
        <Col span={12}>
          <ControlRobot />
          <MapRobot />
        </Col>
        <Col span={12}>
          <CameraStream />
        </Col>
      </Row>
    </div>
  );
}

export default App;
