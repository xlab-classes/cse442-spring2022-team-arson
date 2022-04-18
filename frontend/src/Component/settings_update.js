import React from 'react';
import './settings_update.css';
import Settings from './settings.js'

class SettingsUpdate extends React.Component {
    render () {
        return(
            <>
            <Settings />
            <text className = "updateMessage">ACCOUNT UPDATED</text>
            </>
        );
    }
}

export default SettingsUpdate;