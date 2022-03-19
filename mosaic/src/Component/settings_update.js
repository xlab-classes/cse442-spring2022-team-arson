import React from 'react';
import './settings_update.css';
import Settings from './settings.js'

const SettingsUpdate = () => {
    return(
        <>
        <Settings />
        <text className = "updateMessage">ACCOUNT UPDATED</text>
        </>
    )
}

export default SettingsUpdate;