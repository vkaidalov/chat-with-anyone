import React from "react";

import ContactItem from "./ContactItem";

class ContactList extends React.Component {
    render() {
        return (
            <ul className="contacts__list">
                <ContactItem firstName="Ada" lastName="Lovelace" username="lovelace"/>
                <ContactItem firstName="Zack" lastName="Rider" username="ZackRider"/>
            </ul>
        );
    }
}

export default ContactList;
