import '../App.css';
import menu from "./menu.module.css";
import React, { useState } from 'react';
import MenuShow from './MenuShow';

function Menu() {
  const [show, setShow] = useState(false);

    return (
      <div className="App">
        <header className="App-header">
          <div className={menu.Menu} onClick={() => setShow(currentShow => !currentShow)}>
            <div className={menu.Line1}></div>
            <div className={menu.Line2}></div>
            <div className={menu.Line3}></div>
            { show ? <MenuShow/> : null }
          </div>
          {/* Link to home
          <Link to = "/home">
            <div className={menu.Rectangle1} hidden>
              <text className={menu.Home}>HOME</text>
            </div>
          </Link>
          Link to profile
          <Link to = "/profile/user/test123">
            <div className={menu.Rectangle2} hidden>
              <text className={menu.Profile}>PROFILE</text>
            </div>
          </Link>
          Link to settings
          <Link to = "/settings">
            <div className={menu.Rectangle3} hidden>
              <text className={menu.Settings}>SETTINGS</text>
            </div>
          </Link>
          Link to landing page
          <Link to = "/">
            <div className={menu.Rectangle4} hidden>
              <text className={menu.Logout}>LOG OUT</text>
            </div>
          </Link>
          */}
        </header> 
      </div>
    );
}

export default Menu;

