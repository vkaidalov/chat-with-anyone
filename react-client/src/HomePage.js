import React from "react";
import {Route, Link} from "react-router-dom";

import axios from "./axiosBaseInstance";

import handleInputChange from "./utils";

import UserIcon from "./user-icon.png";
import "./HomePage.css";

import ContactList from "./components/ContactList";
import ChatList from "./components/ChatList";
import MessageList from "./components/MessageList";

class HomePage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username: '',
            firstName: '',
            lastName: '',
            chats: [{
                id: 0,
                name: 'chat #1',
                last_message_at: '2019-09-21T17:08:17.224Z',
                last_message_text: 'Hello!'
            }],
            isChatSelected: false,
            selectedChat: {
                id: 0,
                name: 'chat #1'
            },
            selectedChatMessages: [{
                id: 0,
                username: "username",
                created_at: "2019-09-21T17:08:17.224Z",
                text: "Hello!"
            }],
            newMessageText: ""
        };

        this.fetchUserDetail();
        this.fetchUserChats();

        this.handleInputChange = handleInputChange.bind(this);

        this.handleChatItemClick = this.handleChatItemClick.bind(this);
        this.handleMenuToggleButtonClick = this.handleMenuToggleButtonClick.bind(this);
        this.handleSendMessageButtonClick = this.handleSendMessageButtonClick.bind(this);
        this.handleSignOutButtonClick = this.handleSignOutButtonClick.bind(this);
    }

    componentDidMount() {
        this.timerID = setInterval(
          () => {
              if (this.state.isChatSelected) {
                  this.fetchSelectedChatMessages(
                      this.state.selectedChat.id
                  )
              }
          },
          1000
        );
    }

    componentWillUnmount() {
        clearInterval(this.timerID);
    }

    fetchUserDetail() {
        const userId = localStorage.getItem("userId");
        const token = localStorage.getItem("token");
        axios.get(`api/users/${userId}`, {
            headers: {"Authorization": token}
        })
            .then(response => {
                this.setState({
                    username: response.data["username"],
                    firstName: response.data["first_name"],
                    lastName: response.data["last_name"]
                });
            })
            .catch(() => {
                alert("Error while fetching the user's detail.");
            });
    }

    fetchUserChats() {
        const userId = localStorage.getItem("userId");
        const token = localStorage.getItem("token");
        axios.get(`api/users/${userId}/chats/`, {
            headers: {"Authorization": token}
        })
            .then(response => {
                this.setState({
                    chats: response.data.sort(
                        (a, b) => (a["last_message_at"] > b["last_message_at"]) ? 1 : (
                            (b["last_message_at"] > a["last_message_at"]) ? -1 : 0
                        )
                    ).reverse()
                });
            })
            .catch(() => {
                alert("Error while fetching the user's chats.");
            });
    }

    fetchSelectedChatMessages(selectedChatId) {
        const token = localStorage.getItem("token");
        axios.get(`api/chats/${selectedChatId}/messages/`, {
            headers: {"Authorization": token}
        })
            .then(response => {
                this.setState({
                    selectedChatMessages: response.data.sort(
                        (a, b) => (
                            a["created_at"] > b["created_at"]) ? 1 :
                            ((b["created_at"] > a["created_at"]) ? -1 : 0
                            )
                    )
                });
            })
            .catch(() => {
                alert("Error while fetching your chats.");
            });
    }

    handleChatItemClick(_event, chatId) {
        const selectedChat = this.state.chats.find((element, _index, _array) => {
            return element.id === chatId;
        });
        const selectedChatId = selectedChat.id;
        const selectedChatName = selectedChat.name;

        this.setState({
            isChatSelected: true,
            selectedChat: {
                id: selectedChatId,
                name: selectedChatName
            }
        });
        this.fetchSelectedChatMessages(selectedChatId);
    }

    handleSendMessageButtonClick(_event) {
        _event.preventDefault();
        const token = localStorage.getItem("token");
        const chatId = this.state.selectedChat.id;
        const text = this.state.newMessageText;
        axios.post(`api/chats/${chatId}/messages/`, {text}, {
            headers: {"Authorization": token}
        })
            .then(_response => {
                this.setState({
                    newMessageText: ""
                });
                this.fetchSelectedChatMessages(chatId);
            })
            .catch(_error => {
                alert("Error while sending your message.");
            });
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
        } else if (!toggleButtonInput.checked) {
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
                                       onClick={this.handleMenuToggleButtonClick}/>
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
                            <input name="bar" className="toolbar__item_input" id="contacts" type="radio"/>
                            <label className="toolbar__item_label" htmlFor="contacts">
                                <span>
                                    <Link to={`${this.props.match.url}/contacts`}>Contacts</Link>
                                </span>
                            </label>

                            <input name="bar" className="toolbar__item_input" id="chats" type="radio"
                                   defaultChecked={true}/>
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
                        <Route path={`${this.props.match.url}/contacts`} component={ContactList}/>
                        <Route path={`${this.props.match.url}/chats`}
                               render={
                                   () => <ChatList
                                       chats={this.state.chats} handleChatItemClick={this.handleChatItemClick}
                                   />
                               }
                        />
                    </div>
                </div>

                {this.state.isChatSelected ? (<div className="right-area messenger">
                    <div className="messenger__chat-meta">
                        <div className="chat-meta__info">
                            <h3 className="chat-meta__info_title">
                                {this.state.selectedChat.name}
                            </h3>
                        </div>
                    </div>

                    <div className="messenger__messages">
                        <MessageList messages={this.state.selectedChatMessages} username={this.state.username}/>
                    </div>

                    <div className="messenger__text-area">
                        <form className="text-area_wrapper">
                            <div className="input-field text-area_input">
                                <textarea
                                    id="textarea" className="materialize-textarea"
                                    name="newMessageText" onChange={this.handleInputChange}
                                    value={this.state.newMessageText}
                                />
                            </div>
                            <button
                                className="text-area_button"
                                onClick={this.handleSendMessageButtonClick}
                            />
                        </form>
                    </div>
                </div>) : (
                    <div className="right-area messenger">
                        <div className="messenger__chat-meta">
                            <div className="chat-meta__info">
                                <h3 className="chat-meta__info_title">
                                    Messages will appear here if a chat is selected.
                                </h3>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        );
    }
}

export default HomePage;
