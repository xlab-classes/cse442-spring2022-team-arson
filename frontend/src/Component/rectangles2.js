import React from 'react';
import rectangles from "./rectangles.module.css";

class Rectangles2 extends React.Component {
    render() {
        return (
            <>
            <div className = {rectangles.Rec2_1}></div>
            <div className = {rectangles.Rec2_2}></div>
            <div className = {rectangles.Rec2_3}></div>
            <div className = {rectangles.Rec2_4}></div>
            <div className = {rectangles.Rec2_5}></div>
            <div className = {rectangles.Rec2_6}></div>
            </>
          )
    }
}

export default Rectangles2;