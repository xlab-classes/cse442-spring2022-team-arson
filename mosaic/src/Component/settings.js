import React from 'react';
import {Link} from "react-router-dom";
import './settings.css';
import Logo_Img from './Mosaic Maker.png';
import Rectangles2 from './rectangles2';
import Menu from '../Component/Menu';

class Settings extends React.Component {
  render () {  
    return (
      <>
      <Rectangles2 />
      <img className = "Logo2" src = {Logo_Img} alt = ""></img>
      <div className = "Banner"></div>
      <text className = "BannerText">Mosaic Maker</text>
      <div className = "Border"></div>

      <div className = "Setting"></div>
      <text className = "SettingText">SETTINGS</text>
      <div className = "Box2"></div>
      
      <label className = "currentLabel" for = "currentPass">CURRENT PASSWORD</label>
      <input type = "text" className = "currentInput" name = "currentPass"></input>
      <label className = "newUser1" for = "newUser1">NEW USERNAME</label>
      <input type = "text" className = "userInput1" name = "newUser1"></input>
      <label className = "newUser2" for = "newUser2">RETYPE USERNAME</label>
      <input type = "text" className = "userInput2" name = "newUser2"></input>
      <label className = "newPass1" for = "newPass1">NEW PASSWORD</label>
      <input type = "password" className = "passInput1" name = "newPass1"></input>
      <label className = "newPass2" for = "newPass2">RETYPE PASSWORD</label>
      <input type = "password" className = "passInput2" name = "newPass2"></input>
      <Link to = "/settings/updated"><input type = "submit" className = "updateButton" value = "SUBMIT"></input></Link>
      <Menu />
      </>
    );
  }
}

export default Settings;