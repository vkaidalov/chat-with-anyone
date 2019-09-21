import React from "react";

import ChatItem from "./ChatItem";

class ChatList extends React.Component {
    render() {
        return (
            <ul className="contacts__list">
                <ChatItem/>
                <ChatItem/>
                <ChatItem/>
                <ChatItem/>
                <ChatItem/>
                <ChatItem/>
                <ChatItem/>
                <ChatItem/>
            </ul>
        );
    }
}

export default ChatList;
