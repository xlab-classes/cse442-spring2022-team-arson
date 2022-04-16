import '../App.css';
import './settings.css';
import home from "./home.module.css";
import React from 'react';
import logo from "../assets/MosaicMakerLogo.png";
import Menu from "../Component/Menu";
import Rectangles2 from './rectangles2';
import {Link} from "react-router-dom";

class HomeRandom extends React.Component {
  constructor() {
    super();
    this.state = {
      name: "React"
    };
    this.onChangeValue = this.onChangeValue.bind(this);
  }

  onChangeValue(event) {
    console.log(event.target.value);
  }
    render() {
        return (
            <div className={home.home}>
                <header className={home.header}>
                    <Rectangles2/>
                    <div className={home.logo}> <img src={logo} alt="logo"/></div>
                    <div className={home.titleBG}></div>
                    <text className = {home.BannerText}>Mosaic Maker</text>
                    <div className = {home.Border}></div>
                </header>
                <div className={home.submission}>
                  <div className={home.tabs}>
                    <Link to = "/home/upload" style={{ textDecoration: 'none' }}>
                      <div className={home.uploadbox} >
                        <text className={home.uploadtext}>UPLOAD</text>
                      </div>
                    </Link>
                    <Link to = "/home/keyword" style={{ textDecoration: 'none' }}>
                      <div className={home.keywordbox}>
                        <text className={home.keywordtext}>KEYWORD</text>
                      </div>
                    </Link>
                    <Link to = "/home/random" style={{ textDecoration: 'none' }}>
                      <div className={home.randomboxselected}>
                        <text className={home.randomboxtext}>RANDOM</text>
                      </div>
                    </Link>
                  </div>
                  <div className={home.background}>
                    <div className={home.randomfield}>
                        <div className={home.selections}>
                            <div className={home.randominput}>
                                <text className={home.randomtext}>Random image will be used to create a mosaic</text>
                            </div>
                        </div>
                        <div className={home.selections}></div>
                        <form className={home.selections} onChange={this.onChangeValue} method = "post">
                            <input type="radio" name="privacy" value="Public" className={home.public} checked = "checked"/><text className={home.publictext}>Public</text>
                            <input type="radio" name="privacy" value="Private" className={home.private}/> <text className={home.privatetext}>Private</text>
                            <button className={home.submit} type = "submit">
                              <text className={home.submittext}>SUBMIT</text>
                            </button>
                        </form>
                    </div>
                  </div>
                </div>
                <div className={home.Border2}></div>
                <div className={home.recentimages}>
                  <div className={home.recentimagestab}>
                    <div className={home.recentimagesbox}>
                      <text className={home.recentimagestext}>RECENT IMAGES</text>
                    </div>
                  </div>
                  <div className={home.recentimagesBG}></div>
                </div>
                <Menu />
            </div>
        );
    } 
}

export default HomeRandom