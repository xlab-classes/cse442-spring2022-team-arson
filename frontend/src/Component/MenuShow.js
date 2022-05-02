import '../App.css';
import menu2 from "./menu2.module.css";
//import menu from "./menu.module.css";
import React from 'react';

class MenuShow extends React.Component {
  render() {
    return (
        <div className={menu2.testing}>
          {/*Link to home*/}
          <a href = '/home'>
            <div className={menu2.Rectangle1}>
              <text className={menu2.Home}>HOME</text>
            </div>
          </a>
          {/*Link to profile*/}
          <a href = '/myprofile'>
            <div className={menu2.Rectangle2}>
              <text className={menu2.Profile}>PROFILE</text>
            </div>
          </a>
          {/*Link to settings*/}
          <a href = '/settings'>
            <div className={menu2.Rectangle3}>
              <text className={menu2.Settings}>SETTINGS</text>
            </div>
          </a>
          {/*Link to landing page*/}
          <a href = '/'>
            <div className={menu2.Rectangle4}>
              <text className={menu2.Logout}>LOG OUT</text>
            </div>
          </a>
        </div>
    );
  }
}

export default MenuShow;
