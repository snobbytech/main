import React, { useContext, useState, useEffect } from "react";
import { Route, Redirect } from "react-router-dom";
import { bool, any, object } from "prop-types";
import { auth } from "./base";
import { AuthContext } from "./App";

const ProtectedRouteHoc = ({ component: Component, isLoggedIn, extraProps, ...rest }) => {
  const authContext = useContext(AuthContext);

  if (authContext.authInitialized) {
    if (authContext.isLoggedIn) {
      return (
        <Route
          {...rest}
          render={(props) => {
            console.log(extraProps);
            console.log('take my props', props);
            var fullProps = Object.assign({}, props, extraProps);
            return <Component {...fullProps}></Component>;
          }}
        />
      );
    } else {
      return <Redirect to={{ pathname: "/login_provider" }} />;
    }
  } else {
    // If we don't know our state yet, don't do anything.
    return (<div></div>);
  }
};

ProtectedRouteHoc.propTypes = {
  component: any,
  isLoggedIn: bool,
  rest: object,
  props: object,
};

export default ProtectedRouteHoc;
