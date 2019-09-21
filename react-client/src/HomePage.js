import React from "react";
import {Route, Link} from "react-router-dom";

import axios from "./axiosBaseInstance";

import UserIcon from "./user-icon.png";
import "./HomePage.css";

import ContactList from "./components/ContactList";
import ChatList from "./components/ChatList";

class HomePage extends React.Component {
    constructor(props) {
        super(props);
        this.handleMenuToggleButtonClick = this.handleMenuToggleButtonClick.bind(this);
        this.handleSignOutButtonClick = this.handleSignOutButtonClick.bind(this);
    }

    handleSignOutButtonClick(_event) {
        const userId = localStorage.getItem("userId");
        const token = localStorage.getItem("token");
        axios.post(`api/users/${userId}/sign-out`, {}, {
            headers: {"Authorization": token}
        })
            .then(_response => {
                localStorage.removeItem("userId");
                localStorage.removeItem("token");
                this.props.history.push("/");
            });
    }

    handleMenuToggleButtonClick(_event) {
        let toggleBlock = document.getElementById('menu__toggle_block');
        let toggleButton = document.getElementById('menu__toggle_button');
        let toggleButtonInput = document.getElementById('menu__toggle_input');

        if (toggleButtonInput.checked) {
            toggleBlock.style.left = '-24px';
            toggleBlock.style.opacity = '1';
            toggleButton.style.zIndex = '2';
            toggleButton.style.left = '168px';
        }
        else if (!toggleButtonInput.checked) {
            toggleBlock.style.left = '-340px';
            toggleBlock.style.opacity = '0';
            toggleButton.style.zIndex = '1';
            toggleButton.style.left = '0';
        }
    }

    render() {
        return (
            <div className="wrapper-home">
                <div className="left-area">
                    <div className="menu">
                        <div className="menu__toggle_wrapper">
                            <div className="menu__toggle_button" id="menu__toggle_button">
                                <input type="checkbox" id="menu__toggle_input"
                                       onClick={this.handleMenuToggleButtonClick} />
                                <label className="menu__toggle_hamburger" htmlFor="menu__toggle_input">
                                    <span/><span/><span/>
                                </label>
                            </div>

                            <div className="menu__toggle_block" id="menu__toggle_block">
                                <div/>
                                <div className="user-icon">
                                    <img src={UserIcon} alt=""/>
                                </div>
                                <form className="form">
                                    <div className="form__item">
                                        <label className="form__item_label" htmlFor="username">Username:</label>
                                        <input className="form__item_input validate"
                                               id="username" placeholder="Username" type="text"/>
                                    </div>
                                    <div className="form__item">
                                        <label className="form__item_label" htmlFor="first-name">First name:</label>
                                        <input className="form__item_input validate"
                                               id="first-name" placeholder="First name" type="text"/>
                                    </div>
                                    <div className="form__item">
                                        <label className="form__item_label" htmlFor="last-name">Last name:</label>
                                        <input className="form__item_input validate"
                                               id="last-name" placeholder="Last name" type="text"/>
                                    </div>
                                    <button type="submit" className="form__item btn waves-effect waves-light">Edit
                                    </button>
                                </form>
                                <div/>
                                <button className="menu__toggle_logout btn" onClick={this.handleSignOutButtonClick}>
                                    Sign Out
                                </button>
                            </div>
                        </div>
                        <div className="search">
                            <form className="toolbar__wrapper shadow">
                                <div className="input-field">
                                    <input type="search" className="validate" placeholder="Search"/>
                                </div>
                            </form>
                        </div>
                    </div>

                    <div className="toolbar">
                        <div className="toolbar__wrapper shadow">
                            <input name="bar" className="toolbar__item_input" id="contacts" type="radio" />
                            <label className="toolbar__item_label" htmlFor="contacts">
                                <span>
                                    <Link to={`${this.props.match.url}/contacts`}>Contacts</Link>
                                </span>
                            </label>

                            <input name="bar" className="toolbar__item_input" id="chats" type="radio" defaultChecked={true} />
                            <label className="toolbar__item_label" htmlFor="chats">
                                <span>
                                    <Link to={`${this.props.match.url}/chats`}>Chats</Link>
                                </span>
                            </label>

                            <input name="bar" className="toolbar__item_input" id="stranger" type="radio"/>
                            <label className="toolbar__item_label" htmlFor="stranger">
                                <span>
                                    <Link to={`${this.props.match.url}/stranger`}>Stranger</Link>
                                </span>
                            </label>

                            <div className="toolbar__selected-line"/>
                        </div>
                    </div>

                    <div className="tab-item-list-area">
                        <Route path={`${this.props.match.url}/contacts`} component={ContactList} />
                        <Route path={`${this.props.match.url}/chats`} component={ChatList} />
                    </div>
                </div>

                <div className="right-area messenger">
                    <div className="messenger__chat-meta">
                        <div className="chat-meta__pic">
                            <img src={UserIcon} alt=""/>
                        </div>
                        <div className="chat-meta__info">
                            <h3 className="chat-meta__info_title">Title of this chat|dialog</h3>
                            <p>last seen 1 minute ago</p>
                        </div>
                    </div>

                    <div className="messenger__messages">
                        <ul className="messenger__messages_list">
                            <li className="messages_list_item">
                                <div className="message sender">
                                    <div className="message_pic">
                                        <img className="dialog__pic_user-pic" src={UserIcon} alt=""/>
                                    </div>
                                    <div className="message_context">
                                        <div className="message_title">
                                            <h3 className="chat-meta__info_title">Title of this chat|dialog</h3>
                                        </div>
                                        <div className="message_text">
                                            <p>For years, scientists have explored how people estimate numerical
                                                quantities
                                                without physically counting objects one by one, approximating, for
                                                instance,
                                                how many paintings are displayed on a wall or estimating the number of
                                                players on a football field.
                                                Gaining a deeper understanding of how the process of approximation
                                                occurs in
                                                the brain has become a fertile area of research across numerous
                                                disciplines,
                                                including cognitive psychology education.</p>
                                        </div>
                                        <div className="message_time">
                                            <span className="user-info__time">11:30 PM</span>
                                        </div>
                                    </div>

                                </div>
                            </li>

                            <li className="messages_list_item">
                                <div className="message receiver">
                                    <div className="message_pic">
                                        <img className="dialog__pic_user-pic" src={UserIcon} alt=""/>
                                    </div>
                                    <div className="message_context">
                                        <div className="message_title">
                                            <h3 className="chat-meta__info_title">Client title</h3>
                                        </div>
                                        <div className="message_text">
                                            <p>That means I add up stuff one after the other—serial accumulator—based on
                                                what I see in the center of where I look, as opposed to the edges. So
                                                when
                                                you estimate the number of cars behind you, you are likely moving your
                                                center of gaze around and non-verbally adding up an approximation to the
                                                number.</p>
                                        </div>
                                        <div className="message_time">
                                            <span className="user-info__time">11:31 PM</span>
                                        </div>
                                    </div>
                                </div>
                            </li>

                            <li className="messages_list_item">
                                <div className="message sender">
                                    <div className="message_pic">
                                        <img className="dialog__pic_user-pic" src={UserIcon} alt=""/>
                                    </div>
                                    <div className="message_context">
                                        <div className="message_title">
                                            <h3 className="chat-meta__info_title">Title of this chat|dialog</h3>
                                        </div>
                                        <div className="message_text">
                                            <p>How the process of approximation occurs in the brain has become a fertile
                                                area of research across numerous disciplines, including cognitive
                                                psychology
                                                education.</p>
                                        </div>
                                        <div className="message_time">
                                            <span>11:33 PM</span>
                                        </div>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>

                    <div className="messenger__text-area">
                        <form className="text-area_wrapper">
                            <div className="input-field text-area_input">
                                <textarea id="textarea" className="materialize-textarea"/>
                            </div>
                            <button className="text-area_button"/>
                        </form>
                    </div>
                </div>
            </div>
        );
    }
}

export default HomePage;
