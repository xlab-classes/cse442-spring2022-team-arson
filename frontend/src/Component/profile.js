import React from 'react';
import './profile.css'
import Logo_Img from './Mosaic Maker.png';
import Rectangles2 from './rectangles2';
import Menu from '../Component/Menu.js';
import { useParams } from 'react-router-dom';

const Profile = () => {
    const {user} = useParams();
    
    return (
        <>
        <Rectangles2 />
        <img className = "Logo2" src = {Logo_Img} alt = ""></img>
        <div className = "Banner"></div>
        <text className = "BannerText">Mosaic Maker</text>
        <div className = "Border"></div>

        <div className = "profileBar"></div>
        <text className = "profileText">{user}'s Profile</text>

        <text className = "filterLabel">FILTER:</text>
        <div className = "filterMenu"></div>
        <text className = "filterChoice">WIP</text>
        <text className = "sortLabel">SORT:</text>
        <div className = "sortMenu"></div>
        <text className = "sortChoice">WIP</text>

        <div className = "savedImages"></div>
        <text className = "savedText">SAVED IMAGES</text>
        <div className = "imageBox"></div>

        <Menu />
        </>
    );
}

export default Profile;