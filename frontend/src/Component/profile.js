import React from 'react';
import './profile.css'
import Logo_Img from './Mosaic Maker.png';
import Rectangles2 from './rectangles2';
import Menu from '../Component/Menu.js';
import { useParams } from 'react-router-dom';

const RenderProfile = () => {
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
        </>
    );
}

class Profile extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            items: [],
            filtered: [],
            results: [],
            sortCallback : this.sortDate,
        }
        this.handleDropDown = this.handleDropDown.bind(this)
        this.filterDate = this.filterDate.bind(this)
        this.sortDate = this.sortDate.bind(this)
        this.sortSize = this.sortSize.bind(this)
        // this.sortRandom = this.sortSize.bind(this)
    }

    handleDropDown(e){
        // Event delegation
        // Destructuring e target thing here
        const {nodeName, textContent, parentNode} = e.target
        // Change itself based on button values
        // Change parent node inner text which is itself..
        if (nodeName === 'BUTTON'){
            parentNode.parentNode.firstChild.textContent = textContent
        }
        // Hide button that starts with the name
    }

    // Altenatively press button to send another api request and work it on the backend..

    // Gotta load the first ~6 12 
    // Change resolution of the images for better perf
    // Canvas interactive element

    componentDidMount(){
        // Load from flask api the images...
        fetch(`/profile/images/${window.profile_user}`, {credentials: 'include'})
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        filtered: result,
                        results : result
                    })
                    console.log(result)
                },
                (error) => {}
            )
    }


    // process and filter
    filterDate(elapsedday){
        console.log(`Filtering ${elapsedday}`)
        // Filter the filtered and apply it to results and sort again
        this.setState((previous) => {
            return {results: previous.filtered.filter((item) => {
                var createtime = new Date(0)
                createtime.setUTCSeconds(item.ctime)
                var elapsed = new Date(Date.now() - elapsedday * 24 * 60 * 60 * 1000)  
                return createtime > elapsed
            })}
        })

        var text = document.getElementById("textSort")
        text.textContent = "Date"
        this.sortDate()
    }
    
    sortDate(){
        console.log("Sorting Date")
        this.setState((previous)=>{ return {results: previous.results.sort((a,b) => {return a.ctime - b.ctime})}})
        console.log(this.state.results)
    }
    
    sortSize(){
        console.log("Sorting Size")
        // this.setState((previous)=>{results: previous.results.sort((a,b) => {return a.size - b.size})})
        this.setState((previous)=>{ return {results: previous.results.sort((a,b) => {return b.size - a.size})}})
        console.log(this.state.results)
    }

    render () {
        return (
            <>
            <RenderProfile />

            <div className = "savedImages"></div>
            <text className = "savedText">SAVED IMAGES</text>
            <div className = "imageBox">
                {/* Generate img tags from this.results up to 10 user can click button to load more */}
                {/* Make sure images are within the bound */}
                {/* Can load more */}
                {/* Form Submission -> Results Public -> View Id Public */}
                {/* Form Subbmision to /home/upload saves images redirects to moscaicify */}
                {/* Image sizes are severly effecting perf */}
                {/* {this.state.results.map((image) => <div> image.imageID </div>)} */}
                {this.state.results.map (
                    (image) =>
                        <div className= "image">
                            <a href = {`/view/id/${image.imageID}`}>
                                <img src={`/id/${image.imageID}`} alt={`${image.imageID}`} className="images"/>
                            </a>
                        </div>
                    )
                }
            </div>

            <text className = "filterLabel">FILTER:</text>
            <div className = "filterMenu"></div>
            <div className = "filterChoice" onClick={this.handleDropDown}>
                <text> None </text>
                <div className = "dropDown">
                    <button onClick={() => this.filterDate(365*100)}> None </button>
                    <button onClick={() => this.filterDate(1)}> &lt; Day </button>
                    <button onClick={() => this.filterDate(7)}> &lt; Week </button>
                    <button onClick={() => this.filterDate(31)}> &lt; Month </button>
                </div>
            </div>


            <text className = "sortLabel">SORT:</text>
            <div className = "sortMenu"></div>
            <div className = "sortChoice" onClick={this.handleDropDown}>
                <text id="textSort"> Date </text>
                <div className = "dropDown">
                    <button onClick={() => this.sortDate()}>Date</button>
                    <button onClick={() => this.sortSize()}>Size</button>
                    {/* <button onClick={() => this.sortRandom()}>Random</button> */}
                </div>
            </div>

            <Menu />
            </>
        );
    }
}

export default Profile;