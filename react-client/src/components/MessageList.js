import React from "react";

import MessageItem from "./MessageItem";

class MessageList extends React.Component {
    render() {
        const username = this.props.authUsername;
        const messageListItems = this.props.messages.map(message =>
            <MessageItem
                key={message["id"]}
                username={message["username"]}
                createdAt={message["created_at"]}
                text={message["text"]}
                isUsers={message["username"] === username.toString()}
            />
        );

        return (
            <ul className="messenger__messages_list">
                {messageListItems}
            </ul>
        );
    }
}

export default MessageList;