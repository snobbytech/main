import React, { useState, useEffect } from "react";
import OurHeader from "./components/OurHeader";
import { useMediaQuery } from "react-responsive";

import { makeStyles } from "@material-ui/core/styles";
import { Layout, Space } from "antd";
import { Typography } from "antd";

import { auth } from "./base";
import "antd/dist/antd.css";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import history from "./history.js";

// amplitude stuff.
import amplitude from "amplitude-js";

// Sentry stuff
import * as Sentry from "@sentry/react";
import { Integrations } from "@sentry/tracing";

// Our components.
import GetZip from "./components/GetZip";
import UserPage from "./components/UserPage";
import StartCheckout from "./components/StartCheckout";
import OrderConfirm from "./components/OrderConfirm";



const { Header, Content, Footer } = Layout;

const useStyles = makeStyles((theme) => ({
  ...{
    containerfonts: {
      fontFamily: "avenir book,sans-serif",
      padding: "0px 0px",
    },
    content: {
      background: "#fff",
    },
    footerlettering: {
      color: "gray",
      "@media (max-width: 520px)": {
        fontSize: "12px",
      },
    },
  },
}));

// the idtoken is grabbed from firebase...
// It might need to be refreshed at some point? I'll have to look into this.
export const AuthContext = React.createContext({
  isLoggedIn: false,
  userInfo: {},
  idToken: "",
  authInitialized: false,
  shortUsername: "",
  stripeState: "",
});

function App(props) {
  const classes = useStyles();

  const [gotAuthContext, setGotAuthContext] = useState(false);

  let USING_URL = process.env.REACT_APP_BACKEND_URL;

  let location = window.location.pathname;

  var unsub = auth.onIdTokenChanged(async (user) => {
  });

  // Note: I don't know yet if my react-router thing is the right thing to do. So I should... figure that out.
  // TODO: learn how this routing ish works.

  // spacer size depending on whether mobile or something else
  let spacersize = 20;
  const isTabletOrMobile = useMediaQuery({ query: "(max-width: 520px)" });
  if (isTabletOrMobile) {
    spacersize = 10;
  }

  // Took out ourHeader.

  return (
    <Layout
      className={"layout " + classes.containerfonts}
      theme="light"
      style={{ background: "#fff" }}
    >
      <body className="d-flex flex-column min-vh-100">
        <AuthContext.Provider
          value={{
            isLoggedIn: AuthContext.isLoggedIn,
            userInfo: AuthContext.userInfo,
            idToken: AuthContext.idToken,
            authInitialized: gotAuthContext,
            shortUsername: AuthContext.shortUsername,
            stripeState: AuthContext.stripeState,
          }}
        >
          <Router history={history}>
            <Content className={classes.content}>
              <div
                id="app"
              >
                <Switch>
                <Route
                    path="/"
                    exact
                    render={(props) => <GetZip {...props} />}
                  />

                  <Route
                    path="/z"
                    exact
                    render={(props) => <GetZip {...props} />}
                  />

                  <Route
                    path="/u/:uid"
                    exact
                    render={(props) => <UserPage {...props} />}
                  />
                  <Route
                    path="/startcheckout"
                    exact
                    render={(props) => <StartCheckout {...props} />}
                  />



                </Switch>
              </div>
            </Content>
          </Router>
        </AuthContext.Provider>
        <footer
          className="container mt-auto pt-4 pb-2"
          style={{ textAlign: "center", background: "#fff", color: "gray" }}
        >
          <Space size={spacersize}>
            <div>
              <a
                href="mailto:itsdchen@gmail"
                className={classes.footerlettering + " dlinks"}
              >
                Contact
              </a>{" "}
            </div>
            <div></div>
          </Space>
        </footer>
      </body>
    </Layout>
  );
}

export default App;
