import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './InputArea.css';

function InputArea(props) {

    let label;

    if (props.label) {
        label = <label for={props.id}>{props.label}</label>
        console.log(typeof(props.onChange))
    };

    return (
        <div className="form__item input-field">
          <input
            id={props.id}
            type={props.type}
            className="validate"
            required={props.required}
            placeholder={props.placeholder}
            value={value}
            onChange={props.handleOnChange.bind(event, props.id)}/>
          {label}
        </div>
    );
}

InputArea.propTypes = {
    id: PropTypes.string.isRequired,
    placeholder: PropTypes.string,
    type: PropTypes.string.isRequired,
    required: PropTypes.string,
    label: PropTypes.string,
    onChange: PropTypes.func.isRequired
}

export default InputArea;