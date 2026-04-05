import React, { useState } from "react";
import Login from "./Login";
import Dashboard from "./Dashboard";

const App = () => {
  const [loggedIn, setLoggedIn] = useState(
    !!localStorage.getItem("access")
  );

  return (
    <div>
      {loggedIn ? (
        <Dashboard setLoggedIn={setLoggedIn} />
      ) : (
        <Login setLoggedIn={setLoggedIn} />
      )}
    </div>
  );
};

export default App;