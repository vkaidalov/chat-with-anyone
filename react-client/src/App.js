import React from 'react';
import { BrowserRouter as Router, Route} from "react-router-dom";

import SignInPage from "./SignInPage";
import SignUpPage from "./SignUpPage";
import HomePage from "./HomePage";

class App extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <Router>
                <div>
                    <Route exact path="/" component={SignInPage} />
                    <Route path="/signup" component={SignUpPage} />
                    <Route path="/home" component={HomePage} />
                </div>
            </Router>
        )
    }
}

export default App;
