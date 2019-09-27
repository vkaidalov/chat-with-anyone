import React from "react";
import {Link} from "react-router-dom";

import axios from "./axiosBaseInstance";
import handleInputChange from "./utils";

import UserIcon from "./true-user-icon.png";
import "./SignInSignUpPage.css";

class SignInPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            email: '',
            password: ''
        };
        this.handleInputChange = handleInputChange.bind(this);
        this.handleSignInFormSubmit = this.handleSignInFormSubmit.bind(this);
    }

    handleSignInFormSubmit(event) {
        event.preventDefault();
        const data = {
            email: this.state.email,
            password: this.state.password
        };
        axios.post("api/sign-in", data)
            .then(response => {
                localStorage.setItem("token", response.data["token"]);
                localStorage.setItem("userId", response.data["user_id"]);
                this.props.history.push("/home/chats");
            })
            .catch(error => {
                alert(error.response.data["message"] || error.response.data["email"]);
            });
    }

    render() {
        return (
            <div className="wrapper">
                <div className="user-icon">
                    <img src={UserIcon} alt=""/>
                </div>

                <form className="form" onSubmit={this.handleSignInFormSubmit}>
                    <div className="form__item input-field inline">
                        <input className="form__item_input validate"
                               name="email" onChange={this.handleInputChange}
                               placeholder="E-mail" type="email" required/>
                    </div>

                    <div className="form__item input-field inline">
                        <input className="form__item_input validate"
                               name="password" onChange={this.handleInputChange}
                               placeholder="Password" type="password" required/>
                    </div>

                    <div>
                        <button type="submit" className="form__item btn waves-effect waves-light">
                            Sign In
                        </button>

                        <div className="additional_links">
                            <Link className="register" to="/signup">Sign Up</Link>
                        </div>
                    </div>
                </form>
            </div>
        );
    }
}

export default SignInPage;