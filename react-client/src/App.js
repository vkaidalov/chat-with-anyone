import React from 'react';
import axios from 'axios';

import Toolbar from './components/Toolbar';

import logo from './logo.svg';
import './App.css';

const BASE_URL = 'http://localhost:8000';

class App extends React.Component {
  state = {
    formData: {
      email: '',
      password: '',
    },
    error: null,
    user: {
      token: null,
      user_id: null,
    },
    selectedTab: 'contacts',
  };

  handleAuthDataChange = ({ target: { name, value } }) => {
    this.setState(prevState => ({
      formData: {
        ...prevState.formData,
        [name]: value,
      },
    }));
  };

  handleSubmit = async event => {
    event.preventDefault();

    const {
      formData: { email, password },
    } = this.state;

    try {
      const { data } = await axios.post(`${BASE_URL}/api/sign-in`, {
        email,
        password,
      });

      this.setState({ user: data });
    } catch (err) {
      let message;

      if (err.response === undefined) {
        message = err.message;
      } else {
        message = JSON.stringify(err.response.data);
      }

      this.setState({ error: message });
    }
  };

  handleChangeTab = selected => {
    this.setState({ selectedTab: selected });
  };

  render() {
    const { selectedTab, user, error, formData } = this.state;

    if (error) {
      return <h1 style={{ color: 'red' }}>{error}</h1>;
    }

    if (user.token === null) {
      return (
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <form onSubmit={this.handleSubmit}>
              <label>
                Email:
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={this.handleAuthDataChange}
                />
              </label>
              <br />
              <label>
                Password:
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={this.handleAuthDataChange}
                />
              </label>
              <br />
              <input type="submit" value="Sign In" />
            </form>
          </header>
        </div>
      );
    }

    return (
      <div>
        <Toolbar onTabChange={this.handleChangeTab} selected={selectedTab} />
        {selectedTab === 'contacts' ? null : null}
      </div>
    );
  }
}

export default App;
