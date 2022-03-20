import React from 'react';
import {Link} from "react-router-dom";
import Logo_Img from './Mosaic Maker.png';
import {Rectangles} from '../App.js';
import './logsign.css';

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

const LogSign = () => {
    return (
      <>
      <Rectangles />
      <div className = "Box"></div>
      <img className = "Logo" src = {Logo_Img} alt = ""></img>
      <Link to = "/login"><button className = "Login">LOGIN</button></Link>
      <Link to = "/signup"><button className = "Signup">SIGNUP</button></Link>
      </>
    )
  }

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export default LogSign;