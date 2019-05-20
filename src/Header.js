import React, { Component } from "react";
import { Row, Col, Button, Modal, Input } from "antd";
import request from "./config";
import "./style.css";
import User from "./User";
import * as axios from "axios";
const preUrl = "";

class Header extends Component {
  constructor(props) {
    super(props);
    this.state = {
      isLogin: "",
      username: "",
      password: "",
      visible: false,
      confirmLoading: false,
      error: null
    };
  }

  showModal = () => {
    this.setState({
      visible: true
    });
  };

  handleOk = async event => {
    const user = await request.axios.post(`${preUrl}/login`, {
      username: event.username,
      password: event.password
    });

    User.username = user.data.username;
    User.token = user.data.token;

    this.setState({
        isLogin: this.state.username,
    })

    request.axios = axios.create({
      baseURL: "http://192.168.43.232:5000",
      headers: {
        Authorization: "bearer " + User.token,
        "Content-Type": "application/json"
      }
    });

    this.hideModal();
  };

  hideModal = () => {
    this.setState({
      visible: false
    });
  };

  handleCancel = () => {
    this.setState({
      visible: false
    });
  };

  onUsernameChange = event => {
    this.setState({
      username: event.target.value
    });
  };

  onPasswordChange = event => {
    this.setState({
      password: event.target.value
    });
  };

  render() {
    return (
      <div className="header-page">
        {this.state.isLogin === "" && (
          <Row>
            <Col span={16}>
              {" "}
              <h1 style={{ color: "white", fontWeight: "bold" }}>ROBOT - GROUP 05</h1>{" "}
            </Col>
            <Col span={8}>
              <Button onClick={() => this.showModal()}>Login</Button>
            </Col>
          </Row>
        )}

        {this.state.isLogin !== "" && (
          <Row>
            <Col span={16}>
              {" "}
              <h1 style={{ color: "white", fontWeight: "bold" }}>ROBOT - GROUP 05</h1>{" "}
            </Col>
            <Col span={8}>
                Login as {this.state.isLogin}
            </Col>
          </Row>
        )}

        <Modal
          title={null}
          visible={this.state.visible}
          closable={false}
          onCancel={this.handleCancel}
          onOk={() =>
            this.handleOk({
              username: this.state.username,
              password: this.state.password
            })
          }
          centered
          width="40%"
        >
          <div style={{ padding: "30px" }}>
            <Input
              placeholder="Username"
              onChange={event => this.onUsernameChange(event)}
            />
            <br /> <br />
            <Input
              placeholder="Password"
              onChange={event => this.onPasswordChange(event)}
            />
          </div>
        </Modal>
      </div>
    );
  }
}

export default Header;
