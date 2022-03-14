import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Routes, Route} from "react-router-dom";
import './index.css';
import LogSign from './pages/logsign.js';
import Login from './pages/login.js';
import Signup from './pages/signup.js';
import Settings from './pages/settings.js';
import Menu from './Component/Menu.js';

///////////////////////////////////////////////////////////////////////////////////////////////

const base = document.getElementById("base");

///////////////////////////////////////////////////////////////////////////////////////////////

const App = () =>{
    return (
        <BrowserRouter>
            <Routes>
                <Route index element = {<LogSign />} />
                <Route path = "login" element = {<Login />} />
                <Route path = "signup" element = {<Signup />} />
                <Route path = "settings" element = {<Settings />} />
                <Route path = "menu" element = {<Menu />} />
            </Routes>
        </BrowserRouter>
    );
}

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

ReactDOM.render(<App />, base);

