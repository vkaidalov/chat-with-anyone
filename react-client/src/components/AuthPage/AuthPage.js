import React from 'react';
import './AuthPage.css';
import userPic from '../../assets/img/user-icon.png';
import Register from './Register';


function AuthPage(props) {

    return (
        <div className='wrapper'>
            <div className='user-icon'>
                <img src={userPic} alt='' />
            </div>

            <Register handleOnChange={props.handleOnChange} />

        </div>
    );
}

export default AuthPage;