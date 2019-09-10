import React from 'react';
import PropTypes from 'prop-types';
import './Button.css';

function Button(props) {

    const color = (props.color || 'var(--main-color)');
    const styles = {
        button: {
            color: {color}
        }
    };

    return (
        <div>
            <button
                type={props.type}
                className="form__item btn waves-effect waves-light"
                style={styles.button}>
                {props.text}
            </button>
        </div>
    );
}

Button.propTypes = {
    type: PropTypes.string.isRequired,
    required: PropTypes.string,
    label: PropTypes.string
}

export default Button;