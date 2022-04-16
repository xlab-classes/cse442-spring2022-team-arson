import '../App.css';
import menu2 from "./menu2.module.css";
//import menu from "./menu.module.css";
import {Link} from "react-router-dom";
import React from 'react';

class MenuShow extends React.Component {
  render() {
    return (
        <div className={menu2.testing}>
          {/*Link to home*/}
          <Link to = "/home" style={{ textDecoration: 'none' }}>
            <div className={menu2.Rectangle1}>
              <text className={menu2.Home}>HOME</text>
            </div>
          </Link>
          {/*Link to profile*/}
          <Link to = "/profile/" style={{ textDecoration: 'none' }}>
            <div className={menu2.Rectangle2}>
              <text className={menu2.Profile}>PROFILE</text>
            </div>
          </Link>
          {/*Link to settings*/}
          <Link to = "/settings" style={{ textDecoration: 'none' }}>
            <div className={menu2.Rectangle3}>
              <text className={menu2.Settings}>SETTINGS</text>
            </div>
          </Link>
          {/*Link to landing page*/}
          <Link to = "/" style={{ textDecoration: 'none' }}>
            <div className={menu2.Rectangle4}>
              <text className={menu2.Logout}>LOG OUT</text>
            </div>
          </Link>
        </div>
    );
  }
}

export default MenuShow;
