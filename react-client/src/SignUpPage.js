import React from "react";
import { Link } from "react-router-dom";

import axios from "./axiosBaseInstance";
import handleInputChange from "./utils";

import UserIcon from "./user-icon.png";
import "./SignInSignUpPage.css";

class SignUpPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            email: '',
            password: ''
        };
        this.handleInputChange = handleInputChange.bind(this);
        this.handleSignUpFormSubmit = this.handleSignUpFormSubmit.bind(this);
    }

    handleSignUpFormSubmit(event) {
        event.preventDefault();
        const data = {
            username: this.state.username,
            email: this.state.email,
            password: this.state.password
        };
        axios.post("api/signup", data)
            .then(response => {
                alert("Check your mail and confirm registration.");
                this.props.history.push("/");
            })
            .catch(error => {
                alert(error.response.data["message"] || error.response.data["email"]);
            });
    }

    render() {
        return (
            <div className="wrapper">
                <div className="user-icon">
                    <img src={UserIcon} alt="" />
                </div>

                <form className="form" onSubmit={this.handleSignUpFormSubmit}>
                    <div className="form__item input-field inline">
                        <input className="form__item_input validate"
                            name="username" onChange={this.handleInputChange}
                            placeholder="Username" type="text" required />
                    </div>

                    <div className="form__item input-field inline">
                        <input className="form__item_input validate"
                            name="email" onChange={this.handleInputChange}
                            placeholder="E-mail" type="email" required />
                    </div>

                    <div className="form__item input-field inline">
                        <input className="form__item_input validate"
                            name="password" onChange={this.handleInputChange}
                            placeholder="Password" type="password" required />
                    </div>

                    <div>
                        <button type="submit" className="form__item btn waves-effect waves-light">
                            Sign Up
                        </button>

                        <div className="additional_links">
                            <Link className="register" to="/">Sign In</Link>
                        </div>
                    </div>
                </form>
            </div>
        );
    }
}

export default SignUpPage;