import React from "react";

import ChatItem from "./ChatItem";

class ChatList extends React.Component {
    render() {
        const handleChatItemClick = this.props["handleChatItemClick"];
        const chatListItems = this.props.chats.map(chat =>
            <ChatItem
                key={chat["id"]}
                id={chat["id"]}
                name={chat["name"]}
                lastMessageAt={chat["last_message_at"]}
                lastMessageText={chat["last_message_text"]}
                handleChatItemClick={handleChatItemClick}
            />
        );

        return (
            <ul className="contacts__list">
                {chatListItems}
            </ul>
        );
    }
}

export default ChatList;
