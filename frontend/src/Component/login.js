import React from 'react';
import { render } from 'react-dom';
import {Link} from "react-router-dom";
import './login.css';
import Logo_Img from './Mosaic Maker.png';
import Rectangles from './rectangles';

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Login extends React.Component {
  render() {
    return (
      <>
      <Rectangles />
      <div className = "Box"></div>
      <img className = "Logo1" src = {Logo_Img} alt = ""></img>
      <h1 className = "Heading">WELCOME BACK</h1>
      <label className = "loginLabel" for = "username">USERNAME</label>
      <input type = "text" className = "loginUser" name = "username"></input>
      <label className = "loginLabel1" for = "password">PASSWORD</label>
      <input type = "password" className = "loginPass" name = "password"></input>
      <Link to = "/home"><input type = "submit" className = "loginButton" value = "LOGIN"></input></Link>
      <Link to = "/"><button className = "backButton">BACK</button></Link>
      </>
    );
  }
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export default Login;