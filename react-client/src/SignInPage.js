import React from "react";
import {Link} from "react-router-dom";

import UserIcon from "./user-icon.png";
import "./SignInSignUpPage.css";

function SignInPage() {
    return (
        <div className="wrapper">
            <div className="user-icon">
                <img src={UserIcon} alt=""/>
            </div>

            <form className="form">
                <div className="form__item input-field inline">
                    <input className="form__item_input validate"
                           id="e-mail" placeholder="E-mail" type="email" required/>
                </div>

                <div className="form__item input-field inline">
                    <input className="form__item_input validate"
                           id="password" placeholder="Password" type="password" required/>
                </div>

                <div>
                    <button type="submit" className="form__item btn waves-effect waves-light">Sign In</button>
                    <div className="additional_links">
                        <Link className="register" to="/signup">Sign Up</Link>
                    </div>
                </div>
            </form>
        </div>
    );
}

export default SignInPage;