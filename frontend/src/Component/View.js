import '../App.css';
import view from "./view.module.css";
import React from 'react';
import logo from "../assets/MosaicMakerLogo.png";
import Menu from "../Component/Menu";
import Rectangles2 from './rectangles2';
import { useParams } from 'react-router-dom';
// import {Link} from "react-router-dom";

const View = () => {
    const privacy = useParams();
    const fprivacy = privacy.privacy.toUpperCase();

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
                <img className = {view.fImage} src={`/id/${privacy.id}`} alt="User Post"></img>
            </div>

            <div className = {view.infoBox}>
                <text className = {view.infoText}>Uploaded by: username</text> <br></br>
                <text className = {view.infoText}>Created: MM/DD/YYYY</text> <br></br>
                <text className = {view.infoText}>({privacy.privacy})</text>
            </div>

            <div className = {view.privacyButton}>
                <text className = {view.privacyText}>{fprivacy}</text>
            </div>

            <form method = "post">
                <input type="radio" name="privacy" value="public" className={view.public_input} checked = "checked"/>
                <text className={view.public}>Public</text>
                <input type="radio" name="privacy" value="private" className={view.private_input}/>
                <text className={view.private}>Private</text>
                <button className={view.update} type = "submit">UPDATE</button>
            </form>

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

export default View