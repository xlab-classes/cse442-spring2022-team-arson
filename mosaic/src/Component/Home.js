import '../App.css';
import './settings.css';
import home from "./home.module.css";
import React from 'react';
import logo from "../assets/MosaicMakerLogo.png";
import Menu from "../Component/Menu";
import Rectangles2 from './rectangles2';

class Home extends React.Component {
    render() {
        return (
            <div className={home.home}>
                <header className={home.header}>
                    <Rectangles2/>
                    <div className={home.logo}> <img src={logo} alt="logo"/></div>
                    <div className={home.titleBG}></div>
                    <text className = {home.BannerText}>MOSAIC MAKER</text>
                    <div className = {home.Border}></div>
                </header>



                <div className={home.Border2}></div>
                <Menu />
            </div>
        );
    } 
}

export default Home