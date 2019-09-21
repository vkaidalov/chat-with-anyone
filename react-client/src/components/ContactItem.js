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
                                <span className="user-info__name">firstName lastName</span>
                                <span className="user-info__time">username</span>
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

export default ContactItem;