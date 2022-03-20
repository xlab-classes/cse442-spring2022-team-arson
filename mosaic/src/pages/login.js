import React from 'react';
import {Link} from "react-router-dom";
import './login.css';
import Logo_Img from './Mosaic Maker.png';
import {Rectangles} from '../App.js';

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

const Login = () => {
  return (
    <>
    <Rectangles />
    <div className = "Box"></div>
    <img className = "Logo1" src = {Logo_Img} alt = ""></img>
    <h1 className = "Heading">WELCOME BACK</h1>
    <label className = "loginLabel" for = "username">USERNAME</label>
    <input type = "text" className = "loginUser" name = "username"></input>
    <label className = "loginLabel1" for = "password">PASSWORD</label>
    <input type = "text" className = "loginPass" name = "password"></input>
    <input type = "submit" className = "loginButton" value = "LOGIN"></input>
    <Link to = "/"><button className = "backButton">BACK</button></Link>
    </>
  )
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export default Login;