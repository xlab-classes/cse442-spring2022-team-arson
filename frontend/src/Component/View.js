import '../App.css';
import view from "./view.module.css";
import React from 'react';
import logo from "../assets/MosaicMakerLogo.png";
import Menu from "../Component/Menu";
import Rectangles2 from './rectangles2';
// import {Link} from "react-router-dom";

class View extends React.Component {
    render() {
        return (
            <div className={view.view}>
                <header className={view.header}>
                    <Rectangles2/>
                    <div className={view.logo}> <img src={logo} alt="logo"/></div>
                    <div className={view.titleBG}></div>
                    <text className = {view.BannerText}>Mosaic Maker</text>
                    <div className = {view.Border}></div>
                </header>

                <div className = {view.imageBox}>
                    
                </div>

                <div className = {view.infoBox}>
                    <text className = {view.infoText}>Uploaded by: username</text> <br></br>
                    <text className = {view.infoText}>Created: MM/DD/YYYY</text> <br></br>
                    <text className = {view.infoText}>(public)</text>
                </div>

                <div className = {view.privacyButton}>
                    <text className = {view.privacyText}>PUBLIC</text>
                </div>

                <button className = {view.downloadButton}>
                    <text className = {view.downloadText}>DOWNLOAD</text>
                </button>
                
                <button className = {view.shareButton}>
                    <text className = {view.shareText}>WIP</text>
                </button>

                <Menu />
            </div>
        );
    } 
}

export default View