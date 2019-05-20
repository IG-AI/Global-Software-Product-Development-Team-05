import * as axios from "axios";
import User from "./User";

const request = {
  axios: axios.create({
    baseURL: "http://192.168.43.232:5000",
    headers: {
      Authorization: "bearer " + User.token,
      "Content-Type": "application/json"
    }
  })
};

export default request;
