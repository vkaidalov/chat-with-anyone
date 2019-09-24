import React from "react";
import UserIcon from "../user-icon.png";

class ContactItem extends React.Component {
    render() {
        return (
            <li className="contacts__list_item">
                <div className="dialog inactive">
                    <div className="dialog__main_wrapper">
                        <div className="dialog__pic">
                            <img className="dialog__pic_user-pic" src={UserIcon} alt=""/>
                        </div>
                        <div className="dialog__meta">
                            <div className="user-info">
                                <span className="user-info__name">
                                    {this.props["firstName"]} {this.props["lastName"]}
                                </span>
                                <span className="user-info__time">
                                    {this.props["username"]}
                                </span>
                            </div>
                        </div>
                    </div>
                    {this.props["showSearchResultsMode"] ? (
                        <button
                            className="btn waves-effect waves-light"
                            onClick={
                                (e) => this.props["handleContactSpecialButtonClick"](e, this.props["id"], false)
                            }
                            style={{
                                zIndex: 0,
                                margin: "10px 10px",
                                backgroundColor: "green"
                            }}
                        >
                            Add to Contacts
                        </button>
                    ) : (
                        <div>
                            <button
                                className="btn waves-effect waves-light"
                                onClick={
                                    (e) => this.props["handleContactSpecialButtonClick"](e, this.props["id"], false)
                                }
                                style={{
                                    zIndex: 0,
                                    margin: "10px 10px",
                                    backgroundColor: "green"
                                }}
                                disabled={!this.props["isChatSelected"]}
                            >
                                Add to selected chat
                            </button>
                            <button
                                className="btn waves-effect waves-light"
                                onClick={
                                    (e) => this.props["handleContactSpecialButtonClick"](e, this.props["id"], true)
                                }
                                style={{
                                    zIndex: 0,
                                    margin: "10px 10px",
                                    backgroundColor: "IndianRed"
                                }}
                            >
                                Delete Contact
                            </button>
                        </div>
                    )}
                </div>
            </li>
        );
    }
}

export default ContactItem;