import React from "react";
import UserIcon from "../user-icon.png";

class ChatItem extends React.Component {
    render() {
        return (
            <li className="contacts__list_item">
                <div className="dialog inactive">
                    <div className="dialog__main_wrapper">
                        <div className="dialog__meta">
                            <div className="user-info">
                                <span className="user-info__name">Chat Name</span>
                                <span className="user-info__time">Last message at</span>
                            </div>
                            <div className="dialog__meta_message">
                                <p className="dialog__meta_message_p">Last message text</p>
                            </div>
                        </div>
                    </div>
                    <div className="dialog__options">
                        <span className="option">
                            <span className="option_icon"/>
                            <span className="option_icon"/>
                            <span className="option_icon"/>
                        </span>
                    </div>
                </div>
            </li>
        );
    }
}

export default ChatItem;
