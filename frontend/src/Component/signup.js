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
      <form method = "post">
        <label className = "signupLabel" for="username">USERNAME</label>
        <input type="text" className = "signupUser" name="username"></input>
        <label className = "signupLabel1" for="pass">PASSWORD</label>
        <input type="password" className = "signupPass" name="pass"></input>
        <label className = "signupLabel2" for="pass2">RETYPE PASSWORD</label>
        <input type="password" className = "signupPass2" name="pass2"></input>
        <button className = "signupButton" type="submit">SIGNUP</button>
      </form>
      <Link to = "/"><button className = "backButton">BACK</button></Link>
      </>
    );
  }
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export default Signup;