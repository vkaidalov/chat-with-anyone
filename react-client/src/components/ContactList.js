import React from "react";

import ContactItem from "./ContactItem";

class ContactList extends React.Component {
    render() {
        return (
            <ul className="contacts__list">
                <ContactItem/>
                <ContactItem/>
                <ContactItem/>
                <ContactItem/>
                <ContactItem/>
                <ContactItem/>
                <ContactItem/>
                <ContactItem/>
            </ul>
        );
    }
}

export default ContactList;
