import React from "react";
import UserIcon from "../true-user-icon.png";

class MessageItem extends React.Component {
    render() {
        return (
            <li className="messages_list_item">
                <div className={"message " + (this.props["isUsers"] ? "receiver" : "sender")}>
                    <div className="message_pic">
                        <img className="dialog__pic_user-pic" src={UserIcon} alt=""/>
                    </div>
                    <div className="message_context">
                        <div className="message_title">
                            <h3 className="chat-meta__info_title">{this.props["username"]}</h3>
                        </div>
                        <div className="message_text">
                            <p>{this.props["text"]}</p>
                        </div>
                        <div className="message_time">
                            <span className="user-info__time">{this.props["createdAt"]}</span>
                        </div>
                    </div>
                </div>
            </li>
        );
    }
}

export default MessageItem;