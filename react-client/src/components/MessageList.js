import React from "react";

import MessageItem from "./MessageItem";

class MessageList extends React.Component {
    render() {
        const username = this.props["username"];
        return (
            <ul className="messenger__messages_list">
                {
                    this.props["messages"].map(message =>
                        <MessageItem
                            key={message["id"]}
                            username={message["username"]}
                            createdAt={message["created_at"]}
                            text={message["text"]}
                            isUsers={message["username"] === username}
                        />
                    )
                }
            </ul>
        );
    }
}

export default MessageList;