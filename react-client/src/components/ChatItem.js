import React from "react";

class ChatItem extends React.Component {
    render() {
        return (
            <li className="contacts__list_item"
                onClick={(e) => this.props["handleChatItemClick"](e, this.props.id)}>
                <div className="dialog inactive">
                    <div className="dialog__main_wrapper">
                        <div className="dialog__meta">
                            <div className="user-info">
                                <span className="user-info__name">{this.props.name}</span>
                                <span className="user-info__time">{this.props["lastMessageAt"]}</span>
                            </div>
                            <div className="dialog__meta_message">
                                <p className="dialog__meta_message_p">
                                    {this.props["lastMessageText"] || ""}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </li>
        );
    }
}

export default ChatItem;
