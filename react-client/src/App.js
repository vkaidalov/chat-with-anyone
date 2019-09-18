import axios from 'axios';
import React from 'react';

import logo from './logo.svg';
import './App.css';

const BASE_URL = 'http://localhost:8000';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
      password: '',
      responseData: 'Waiting for Sign In.'
    };

    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleEmailChange(event) {
    this.setState({email: event.target.value});
  }

  handlePasswordChange(event) {
    this.setState({password: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();

    const self = this;
    axios.post(`${BASE_URL}/api/sign-in`, {
      email: self.state.email,
      password: self.state.password
    })
    .then(function (response) {
      self.setState({responseData: `Received token ${response.data.token}.`});
    })
    .catch(function (error) {
      if (!(error.response && error.response.data)) {
        self.setState({responseData: "Can't read response data."});
        return;
      }
      self.setState({
        responseData: JSON.stringify(error.response.data)
      });
    });
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <form onSubmit={this.handleSubmit}>
            <label>
              Email:
              <input type="email" value={this.state.email}
                     onChange={this.handleEmailChange}
              />
            </label>
            <br />
            <label>
              Password:
              <input type="password" value={this.state.password}
                     onChange={this.handlePasswordChange}
              />
            </label>
            <br />
            <input type="submit" value="Sign In" />
          </form>
          <p>Response Data: {this.state.responseData}</p>
        </header>
      </div>
    );
  }
}

export default App;
