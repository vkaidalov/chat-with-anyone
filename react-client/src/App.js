import React, { useState } from 'react';
import AuthPage from './components/AuthPage/AuthPage';

function App() {

  const [authData, setData] = React.useState({
      username: '',
      email: '',
      password: ''
    }
  )

  function handleOnChange(event, fieldName) {
    if (event.target.value.length > 0) {
        console.log(fieldName)
    }
  }


  return (
    <div className="root">
      <AuthPage handleOnChange={handleOnChange} />
    </div>
  );
}

export default App;
