import React from 'react';

import './styles.css';

function Toolbar(props) {
    const { selected, onTabChange } = props;

    return (
        <div className="toolbar">
            <div className="toolbar__wrapper shadow">
                <input
                    name="bar"
                    className="toolbar__item_input"
                    id="contacts"
                    type="radio"
                    checked={selected === 'contacts'}
                    onChange={() => {
                        onTabChange('contacts');
                    }}
                />
                <label className="toolbar__item_label" htmlFor="contacts">
                    <span>Contacts</span>
                </label>
                <input
                    name="bar"
                    className="toolbar__item_input"
                    id="chats"
                    type="radio"
                    checked={selected === 'chats'}
                    onChange={() => {
                        onTabChange('chats');
                    }}
                />
                <label className="toolbar__item_label" htmlFor="chats">
                    <span>Chats</span>
                </label>

                <div className="toolbar__selected-line" />
            </div>
        </div>
    );
}

export default Toolbar;
