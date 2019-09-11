import React from 'react';
import './AuthPage.css';
import userPic from '../../assets/img/user-icon.png';
import Register from './Register';


function AuthPage(props) {

    const [userData, setData] = React.useState({
        username: '',
        email: '',
        password: ''
    });

    function onChangeHandler(e, id) {
        if (e.target.value.length !== 0) {
            setData({id: e.target.value})
        }
    }

    function submitHandler(event) {
        let body = {
            'username': event.target[0].value,
            'email': event.target[1].value,
            'password': event.target[2].value
        };
        event.preventDefault();

        const xhr = new XMLHttpRequest()
        xhr.addEventListener('load', () => {
            console.log(xhr.responseText)
        })
        xhr.open('POST', 'https://http://localhost:8000/api/signup')
        xhr.withCredentials = true;
        xhr.setRequestHeader("Acces-Control-Allow-Origin", "*");
        xhr.setRequestHeader(
            "Acces-Control-Allow-Headers",
            "Origin, X-Requested-With, Content-Type, Accept");
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        
        xhr.send(JSON.stringify(body))

        console.log('username:' + event.target[0].value);
        console.log('email:' + event.target[1].value);
        console.log('password:' + event.target[2].value);
    }

    return (
        <div className='wrapper'>
            <div className='user-icon'>
                <img src={userPic} alt='' />
            </div>

            <Register 
                onChangeHandler={onChangeHandler}
                data={userData}
                submitHandler={submitHandler} />

        </div>
    );
}

export default AuthPage;