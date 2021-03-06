import '../App.css';
import results from "./results.module.css";
import React from 'react';
import logo from "../assets/MosaicMakerLogo.png";
import Menu from "../Component/Menu";
import Rectangles2 from './rectangles2';
import { useParams } from 'react-router-dom';

const Results = () => {
        const userimage = useParams()

        return (
            <div className={results.results}>
                <header className={results.header}>
                    <Rectangles2/>
                    <img className={results.logo} src={logo} alt="logo"/>
                    <div className={results.titleBG}></div>
                    <text className = {results.BannerText}>Mosaic Maker</text>
                    <div className = {results.Border}></div>
                </header>

                <div className = {results.resultsBox}>
                    <text className = {results.resultsText}>RESULTS</text>
                </div>

                <div className = {results.imageBox}>
                    <img className = {results.resultImage} src={`/image/${userimage.userimage}`} alt="User Post"></img>
                </div>

                <form method = "post">
                    <button className = {results.uploadButton}>
                        <text className = {results.uploadText}>UPLOAD</text>
                    </button>
                </form>

                <a href = {`/downloadResult/${userimage.userimage}`}>
                    <button className = {results.downloadButton}>
                        <text className = {results.downloadText}>DOWNLOAD</text>
                    </button>
                </a>
                
                <Menu />
            </div>
        );
    }

export default Results