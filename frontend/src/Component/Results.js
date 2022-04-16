import '../App.css';
import results from "./results.module.css";
import React from 'react';
import logo from "../assets/MosaicMakerLogo.png";
import Menu from "../Component/Menu";
import Rectangles2 from './rectangles2';
import {Link} from "react-router-dom";

class Results extends React.Component {
    render() {
        return (
            <div className={results.results}>
                <header className={results.header}>
                    <Rectangles2/>
                    <div className={results.logo}> <img src={logo} alt="logo"/></div>
                    <div className={results.titleBG}></div>
                    <text className = {results.BannerText}>Mosaic Maker</text>
                    <div className = {results.Border}></div>
                </header>

                <div className = {results.resultsBox}>
                    <text className = {results.resultsText}>RESULTS</text>
                </div>

                <div className = {results.imageBox}>
                    
                </div>

                <form method = "post">
                    <button className = {results.uploadButton}>
                        <text className = {results.uploadText}>UPLOAD</text>
                    </button>
                </form>

                <button className = {results.downloadButton}>
                    <text className = {results.downloadText}>DOWNLOAD</text>
                </button>
                
                <Menu />
            </div>
        );
    } 
}

export default Results