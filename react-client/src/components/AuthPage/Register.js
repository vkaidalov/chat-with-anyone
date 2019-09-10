import React from 'react';
import InputArea from './InputArea';
import './LogIn.css';

function Register(props) {

    function submitHandler(event) {
        event.preventDefault();
        console.log('email:' + event.state.email);
        console.log('password:' + event.state.password);
    }


    return (
        <form className='form' onSubmit={submitHandler}>
            <InputArea 
                id='username'
                type='text'
                label='Username'
                onChange={props.handleOnChange}/>

            <InputArea 
                id='e-mail'
                type='email'
                label='E-mail'
                onChange={props.handleOnChange} />

            <InputArea 
                id='password' 
                type='password'
                label='Password'
                onChange={props.handleOnChange} />

            <div>
            <button
                type='submit'
                className="form__item btn waves-effect waves-light">
                Sign Up
            </button> 
        </div>
        </form>
    );
}

export default Register;