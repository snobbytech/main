import React from "react";
import ReactDOM from "react-dom";
import "./css/custom.scss"; // This is the file to override react-bootstrap primary colors for when we used the styled components
import "./css/normalize.css";
import "./css/index.css"; // This is the majority of our custom css code
import App from "./App";
import * as serviceWorker from "./serviceWorker";

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
