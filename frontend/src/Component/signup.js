import React from 'react';
import {Link} from "react-router-dom";
import './signup.css';
import Logo_Img from './Mosaic Maker.png';
import Rectangles from './rectangles';

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

class Signup extends React.Component {
  render () {
    return (
      <>
      <Rectangles />
      <div className = "Box"></div>
      <img className = "Logo1" src = {Logo_Img} alt = ""></img>
      <label className = "signupLabel" for = "username">USERNAME</label>
      <input type = "text" className = "signupUser" name = "username"></input>
      <label className = "signupLabel1" for = "password">PASSWORD</label>
      <input type = "password" className = "signupPass" name = "password"></input>
      <label className = "signupLabel2" for = "password">RETYPE PASSWORD</label>
      <input type = "password" className = "signupPass2" name = "password2"></input>
      <Link to = "/login"><input type = "submit" className = "signupButton" value = "SIGNUP"></input></Link>
      <Link to = "/"><button className = "backButton">BACK</button></Link>
      </>
    );
  }
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export default Signup;