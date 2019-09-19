import React, { setState } from 'react';
import InputArea from './InputArea';
import './LogIn.css';

function Register(props) {

    return (
        <form className='form' onSubmit={props.submitHandler}>
            <InputArea 
                id='username'
                type='text'
                label='Username'
                name='username'
                value={props.data.username}
                onChange={props.onChangeHandler}/>

            <InputArea 
                id='e-mail'
                type='email'
                label='E-mail'
                value={props.data.email}
                onChange={props.onChangeHandler} />

            <InputArea 
                id='password' 
                type='password'
                label='Password'
                value={props.data.password}
                onChange={props.onChangeHandler} />

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