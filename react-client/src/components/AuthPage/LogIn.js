import React from 'react';
import InputArea from './InputArea';
import './LogIn.css';


export default function LogIn() {
    return (
        <form className='form'>
            <InputArea id='e-mail' type='email' label='E-mail' />
            <InputArea id='password' type='password' label='Password' />

            <div>
            <button
                type='submit'
                className="form__item btn waves-effect waves-light">
                Sign In
            </button>
            <div className="additional_links">
                <a className="register" href="#">Register</a>
                <a className="password" href="#">Password?</a>
            </div>  
        </div>
        </form>
    );
}
