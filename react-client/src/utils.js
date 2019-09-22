function handleInputChange(event) {
    const target = event.target;
    const name = target.name;
    let value;

    switch (target.type) {
        case "checkbox":
            value = target.checked;
            break;
        case "select-multiple":
            value = [];
            for (let i = 0; i < target.options.length; i++) {
                const option = target.options[i];
                if (option.selected) {
                    value.push(option.value);
                }
            }
            break;
        default:
            value = target.value;
            break;
    }

    this.setState({
        [name]: value
    });
}

export default handleInputChange;