import React from "react";

import ContactItem from "./ContactItem";


class ContactList extends React.Component {
    render() {
        const contactListItems = this.props["contacts"].map(contact =>
            <ContactItem
                key={contact["id"]}
                id={contact["id"]}
                username={contact["username"]}
                firstName={contact["first_name"]}
                lastName={contact["last_name"]}
                showSearchResultsMode={this.props["showSearchResultsMode"]}
                isChatSelected={this.props["isChatSelected"]}
                handleContactSpecialButtonClick={this.props["handleContactSpecialButtonClick"]}
            />
        );

        return (
            <ul className="contacts__list">
                {contactListItems}
            </ul>
        );
    }
}

export default ContactList;
