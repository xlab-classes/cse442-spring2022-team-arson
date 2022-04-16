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
      <form method = "post">
        <label className = "loginLabel" for="username">USERNAME</label>
        <input type="text" className = "loginUser" name="username"></input>
        <label className = "loginLabel1" for="pass">PASSWORD</label>
        <input type="password" className = "loginPass" name="pass"></input>
        <button className = "loginButton" type="submit">LOGIN</button>
      </form>
      <Link to = "/"><button className = "backButton">BACK</button></Link>
      </>
    );
  }
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export default Login;