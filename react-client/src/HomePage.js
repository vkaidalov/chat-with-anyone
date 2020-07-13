import React from "react";
import {Route, Link} from "react-router-dom";

import axios from "./axiosBaseInstance";

import handleInputChange from "./utils";

import UserIcon from "./true-user-icon.png";
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
            searchText: '',
            showSearchResultsMode: false,
            searchResultUsers: [{
                id: 0,
                username: "username",
                first_name: "firstName",
                last_name: "lastName"
            }],
            searchResultChats: [{
                id: 0,
                name: "search result chat #1"
            }],
            contacts: [{
                id: 0,
                username: "username",
                first_name: "firstName",
                last_name: "lastName"
            }],
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
        this.fetchUserContacts();
        this.fetchUserChats();

        this.handleInputChange = handleInputChange.bind(this);

        this.handleContactSpecialButtonClick = this.handleContactSpecialButtonClick.bind(this);
        this.handleChatItemClick = this.handleChatItemClick.bind(this);
        this.handleMenuToggleButtonClick = this.handleMenuToggleButtonClick.bind(this);
        this.handleSendMessageButtonClick = this.handleSendMessageButtonClick.bind(this);
        this.handleCreateNewChatButtonClick = this.handleCreateNewChatButtonClick.bind(this);
        this.handleLeaveChatButtonClick = this.handleLeaveChatButtonClick.bind(this);
        this.handleJoinChatButtonClick = this.handleJoinChatButtonClick.bind(this);
        this.handleSearchFormSubmit = this.handleSearchFormSubmit.bind(this);
        this.handleSignOutButtonClick = this.handleSignOutButtonClick.bind(this);
        this.handleEditProfileFormSubmit = this.handleEditProfileFormSubmit.bind(this);
    }

    componentDidMount() {
        this.timerID = setInterval(
            () => {
                if (!this.state.showSearchResultsMode) {
                    this.fetchUserChats();
                }
            },
            1000
        );

        const token = localStorage.getItem("token");

        // TODO: get the server address from an env variable
        const ws = new WebSocket(
            (window.location.protocol === 'https:' ? 'wss://' : 'ws://')
            + `localhost:8000/api/ws/${token}`
        );

        ws.onopen = () => {
            console.log('ws connected.');
        };

        ws.onmessage = (e) => {
            const data = JSON.parse(e.data);
            switch (data['type']) {
                case 'message':
                    const message = data['data'];
                    if (
                        this.state.isChatSelected &&
                        message['room_id'] === this.state.selectedChat.id
                    ) {
                        this.setState({
                            selectedChatMessages: this.state.selectedChatMessages.concat(
                                message
                            )
                        });
                    }
                    break;
                default:
                    alert("Unrecognised type of message's been received via WebSocket.");
            }
        };

        ws.onclose = () => {
            alert(
                'WebSocket connection has been suddenly closed. ' +
                'Try refreshing the page.'
            );
        };

        ws.onerror = () => {
            alert(
                'An error with WebSocket suddenly occurred. ' +
                'Try refreshing the page.'
            );
        };
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

    fetchUserContacts() {
        const userId = localStorage.getItem("userId");
        const token = localStorage.getItem("token");
        axios.get(`api/users/${userId}/contacts/`, {
            headers: {"Authorization": token}
        })
            .then(response => {
                this.setState({
                    contacts: response.data
                });
            })
            .catch(() => {
                alert("Error while fetching the user's contacts.");
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
                    chats: response.data
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
                    selectedChatMessages: response.data
                });
            })
            .catch(() => {
                alert("Error while fetching your chats.");
            });
    }

    handleContactSpecialButtonClick(_event, contactId, deleteMode) {
        const userId = localStorage.getItem("userId");
        const token = localStorage.getItem("token");
        if (this.state.showSearchResultsMode) {
            // adding a user to the user's contact list
            axios.post(`api/users/${userId}/contacts/`, {
                contact_id: contactId
            }, {
                headers: {"Authorization": token}
            })
                .then(_response => {
                    alert("The user has been successfully added to your contact list.");
                    this.fetchUserContacts();
                })
                .catch(_error => {
                    alert("Error while adding the user to your contact list. " +
                        "You've done it already, haven't you?"
                    );
                });
        } else {
            if (deleteMode) {
                // deleting a user from the user's contact list
                axios.delete(`api/users/${userId}/contacts/${contactId}`, {
                    headers: {"Authorization": token}
                })
                    .then(_response => {
                        alert("The user has been successfully deleted from your contact list.");
                        this.fetchUserContacts();
                    })
                    .catch(_error => {
                        alert("Error while deleting the user from your contact list.");
                    });
            } else {
                // adding a user to the selected chat
                axios.post(`api/chats/${this.state.selectedChat.id}/users/`, {
                    user_id: contactId
                }, {
                    headers: {"Authorization": token}
                })
                    .then(_response => {
                        alert("The user has been successfully added to the selected chat on the right.");
                    })
                    .catch(_error => {
                        alert("Error while adding the user to the selected chat on the right. " +
                            "You've done it already, haven't you?"
                        );
                    });
            }
        }
    }

    handleChatItemClick(_event, chatId) {
        const chats = this.state.showSearchResultsMode ?
            this.state.searchResultChats : this.state.chats;

        const selectedChat = chats.find((element, _index, _array) => {
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

        if (this.state.showSearchResultsMode) {
            this.setState({
                selectedChatMessages: []
            });
        } else {
            this.fetchSelectedChatMessages(selectedChatId);
        }
    }

    handleSendMessageButtonClick(event) {
        event.preventDefault();
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
            })
            .catch(_error => {
                alert("Error while sending your message.");
            });
    }

    handleCreateNewChatButtonClick(_event) {
        const chatName = prompt("Enter a name for a new chat:");
        if (!chatName) {
            return;
        }
        const token = localStorage.getItem("token");
        axios.post(`api/chats/`, {name: chatName}, {
            headers: {"Authorization": token}
        })
            .then(_response => {
                this.fetchUserChats();
            })
            .catch(_error => {
                alert("Error while creating a new chat.");
            });
    }

    handleLeaveChatButtonClick(_event) {
        if (!window.confirm("Are you sure you want to leave this chat?")) {
            return;
        }
        this.setState({
            isChatSelected: false
        });
        const userId = localStorage.getItem("userId");
        const token = localStorage.getItem("token");
        const chatId = this.state.selectedChat.id;
        axios.delete(`api/chats/${chatId}/users/${userId}`, {
            headers: {"Authorization": token}
        })
            .then(_response => {
                // nothing!
            })
            .catch(_error => {
                alert("Error while leaving the selected chat.");
            });
    }

    handleJoinChatButtonClick(_event) {
        const userId = localStorage.getItem("userId");
        const token = localStorage.getItem("token");
        const chatId = this.state.selectedChat.id;
        axios.post(`api/chats/${chatId}/users/`, {
            user_id: userId
        }, {
            headers: {"Authorization": token}
        })
            .then(_response => {
                alert("You've successfully joined the chat!");
            })
            .catch(_error => {
                alert("Error while joining the chat. Haven't you joined it yet?");
            });
    }

    handleSearchFormSubmit(event) {
        event.preventDefault();
        if (this.state.searchText === "") {
            this.setState({
                isChatSelected: false,
                showSearchResultsMode: false
            });
            return;
        }
        this.setState({
            isChatSelected: false,
            showSearchResultsMode: true
        });
        const token = localStorage.getItem("token");

        axios.get(`api/users/?username=${this.state.searchText}`, {
            headers: {"Authorization": token}
        })
            .then(response => {
                this.setState({
                    searchResultUsers: response.data
                });
            });

        axios.get(`api/chats/?name=${this.state.searchText}`, {
            headers: {"Authorization": token}
        })
            .then(response => {
                this.setState({
                    searchResultChats: response.data
                });
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

    handleEditProfileFormSubmit(event) {
        event.preventDefault();
        const userId = localStorage.getItem("userId");
        const token = localStorage.getItem("token");

        axios.patch(`api/users/${userId}`, {
            username: this.state.username,
            first_name: this.state.firstName,
            last_name: this.state.lastName
        }, {
            headers: {"Authorization": token}
        })
            .then(_response => {
                alert("Changes were successfully applied.");
            })
            .catch(error => {
                alert(error.response.data["message"]);
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
            toggleButton.style.left = '268px';
        } else if (!toggleButtonInput.checked) {
            toggleBlock.style.left = '-340px';
            toggleBlock.style.opacity = '0';
            toggleButton.style.zIndex = '1';
            toggleButton.style.left = '0';
        }
    }

    handleToolbarLinkClick() {
        document.getElementById(this.className).checked = true;
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
                                <form className="form" onSubmit={this.handleEditProfileFormSubmit}>
                                    <div className="form__item">
                                        <label className="form__item_label" htmlFor="username">Username:</label>
                                        <input className="form__item_input validate"
                                               onChange={this.handleInputChange}
                                               value={this.state.username}
                                               name="username"
                                               id="username" placeholder="Username" type="text"/>
                                    </div>
                                    <div className="form__item">
                                        <label className="form__item_label" htmlFor="first-name">First name:</label>
                                        <input className="form__item_input validate"
                                               onChange={this.handleInputChange}
                                               value={this.state.firstName}
                                               name="firstName"
                                               id="first-name" placeholder="First name" type="text"/>
                                    </div>
                                    <div className="form__item">
                                        <label className="form__item_label" htmlFor="last-name">Last name:</label>
                                        <input className="form__item_input validate"
                                               onChange={this.handleInputChange}
                                               value={this.state.lastName}
                                               name="lastName"
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
                            <form className="toolbar__wrapper shadow" onSubmit={this.handleSearchFormSubmit}>
                                <div className="input-field">
                                    <input
                                        name="searchText" onChange={this.handleInputChange}
                                        type="search" className="validate" placeholder="Search"
                                    />
                                </div>
                            </form>
                        </div>
                    </div>

                    <div className="toolbar">
                        <div className="toolbar__wrapper shadow">
                            <input name="bar" className="toolbar__item_input" id="contacts" type="radio"/>
                            <label className="toolbar__item_label" htmlFor="contacts" onClick={(e) => {
                                e.preventDefault()
                            }}>
                                <span>
                                    <Link to={`${this.props.match.url}/contacts`}
                                          className="contacts"
                                          onClick={this.handleToolbarLinkClick}
                                    >Contacts</Link>
                                </span>
                            </label>

                            <input name="bar" className="toolbar__item_input" id="chats" type="radio"
                                   defaultChecked={true}/>
                            <label className="toolbar__item_label" htmlFor="chats" onClick={(e) => {
                                e.preventDefault()
                            }}>
                                <span>
                                    <Link to={`${this.props.match.url}/chats`}
                                          className="chats"
                                          onClick={this.handleToolbarLinkClick}
                                    >Chats</Link>
                                </span>
                            </label>

                            <div className="toolbar__selected-line"/>
                        </div>
                    </div>

                    <div className="tab-item-list-area">
                        <Route path={`${this.props.match.url}/contacts`}
                               render={
                                   () => <ContactList
                                       contacts={
                                           this.state.showSearchResultsMode ?
                                               this.state.searchResultUsers :
                                               this.state.contacts
                                       }
                                       showSearchResultsMode={this.state.showSearchResultsMode}
                                       isChatSelected={this.state.isChatSelected}
                                       handleContactSpecialButtonClick={this.handleContactSpecialButtonClick}
                                   />
                               }
                        />
                        <Route path={`${this.props.match.url}/chats`}
                               render={
                                   () => this.state.showSearchResultsMode ? (
                                       <div>
                                           <ChatList
                                               chats={this.state.searchResultChats}
                                               handleChatItemClick={this.handleChatItemClick}
                                           />
                                       </div>
                                   ) : (
                                       <div>
                                           <button
                                               className="btn waves-effect waves-light"
                                               onClick={this.handleCreateNewChatButtonClick}
                                               style={{
                                                   zIndex: 0,
                                                   margin: "10px 10px",
                                                   width: "96%"
                                               }}
                                           >
                                               Create New Chat
                                           </button>
                                           <ChatList
                                               chats={this.state.chats}
                                               handleChatItemClick={this.handleChatItemClick}
                                           />
                                       </div>
                                   )
                               }
                        />
                    </div>
                </div>

                {this.state.isChatSelected ? (<div className="right-area messenger">
                    <div className="messenger__chat-meta" style={{justifyContent: "space-between"}}>
                        <div className="chat-meta__info">
                            <h3 className="chat-meta__info_title">
                                {this.state.selectedChat.name}
                            </h3>
                        </div>
                        {this.state.showSearchResultsMode ? (
                            <button
                                className="btn waves-effect waves-light"
                                onClick={this.handleJoinChatButtonClick}
                                style={{
                                    zIndex: 0,
                                    margin: "10px 10px",
                                    float: "right",
                                    backgroundColor: "green"
                                }}
                            >
                                Join Chat
                            </button>
                        ) : (
                            <button
                                className="btn waves-effect waves-light"
                                onClick={this.handleLeaveChatButtonClick}
                                style={{
                                    zIndex: 0,
                                    margin: "10px 10px",
                                    float: "right",
                                    backgroundColor: "IndianRed"
                                }}
                            >
                                Leave Chat
                            </button>
                        )}
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
                                    disabled={this.state.showSearchResultsMode}
                                />
                            </div>
                            <button
                                className="text-area_button"
                                onClick={this.handleSendMessageButtonClick}
                                disabled={this.state.showSearchResultsMode}
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
