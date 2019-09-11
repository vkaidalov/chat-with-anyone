import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './InputArea.css';

function InputArea({id, type, required, placeholder, label, onChange, value}) {

  if (label) {
      label = <label for={id}>{label}</label>
  };
  
  return (
      <div className="form__item input-field">
        <input
          id={id}
          type={type}
          className="validate"
          required={required}
          placeholder={placeholder}
          value={value}
          onChange={(e) => onChange(e, id)}/>
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