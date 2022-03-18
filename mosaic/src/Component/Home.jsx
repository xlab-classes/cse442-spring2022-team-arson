import '../App.css';
import home from "./home.module.css";
import React from 'react';
import logo from "../assets/MosaicMakerLogo.png"
import menu from "./menu.module.css";

class Home extends React.Component {
    render() {
        return (
            <div className={home.home}>
                <header className={home.header}>
                    <div className={home.logo}> <img src={logo} alt="logo"/></div>
                    <div className={home.titleBG}>
                        <text className={home.title}>Mosaic Maker</text>
                    </div>
                    <div className={menu.Menu}>
          <div className={menu.Line1}></div>
          <div className={menu.Line2}></div>
          <div className={menu.Line3}></div>
        </div>
        <div className={menu.Rectangle1} hidden>
          <text className={menu.Home}>HOME</text>
        </div>
        <div className={menu.Rectangle2} hidden>
          <text className={menu.Profile}>PROFILE</text>
        </div>
        <div className={menu.Rectangle3} hidden>
          <text className={menu.Settings}>SETTINGS</text>
        </div>
        <div className={menu.Rectangle4} hidden>
          <text className={menu.Logout}>LOG OUT</text>
        </div>
                </header>
                <div className={home.line1}></div>
            </div>
        );
    } 
}

export default Home