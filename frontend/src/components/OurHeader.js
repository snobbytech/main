import React, { useContext, useEffect } from "react";

import { auth } from "../base";
import { AuthContext } from "../App";

import { withRouter, useHistory, useLocation } from "react-router-dom";

function OurHeader(props) {
  const history = useHistory();
  const location = useLocation();

  const currentPath = location.pathname;
  let headerBackgroundColor = "white";
  if (currentPath == "/") {
    headerBackgroundColor = "#f8faff";
  }

  const authContext = useContext(AuthContext);

  function logout() {
    auth.signOut();
    //console.log("Hey... I should have logged out, yeah");
    authContext.isLoggedIn = false;
    authContext.userInfo = {};
    authContext.shortUsername = "";
    authContext.stripeState = "";
    history.push({
      pathname: "/",
    });
  }

  function handleMe() {
    // Get the short_username.
    if (authContext.shortUsername) {
      history.push({
        pathname: "/p/" + authContext.shortUsername,
      });
    }
  }

  // want to call e.stopPropagation on all of them so that clicking on
  // the hamburger menu dropdown doesn't click on the other elements

  function myBookings(e) {
    e.stopPropagation();
    // Redirect to my bookings.
    history.push({
      pathname: "/mybookings",
    });
  }

  function handleEditBasicProfile(e) {
    e.stopPropagation();
    history.push({
      pathname: "/edit_basic_profile",
    });
  }

  function handleEditAvailability(e) {
    e.stopPropagation();
    history.push({
      pathname: "/edit_availability",
    });
  }

  function handleEditAvailableTasks(e) {
    e.stopPropagation();
    history.push({
      pathname: "/edit_available_tasks",
    });
  }

  function handleLogin(e) {
    e.stopPropagation();
    history.push({
      pathname: "/login_provider",
    });
  }

  function handleSignup(e) {
    e.stopPropagation();
    history.push({
      pathname: "/signup_provider",
    });
  }

  useEffect(() => {}, []);

  useEffect(() => {
    if (authContext.isLoggedIn) {
      //      console.log("Inside ourHeader, our authContext looks like ", authContext);
      if (props.meLink) {
        authContext.shortUsername = props.meLink;
      }
    }
  }, [authContext, props.meLink]);

  const loggedOutMenu = (
    <ul class="navbar-nav ml-auto flex-nowrap">
      <li class="nav-item header-margin header-login" onClick={handleLogin}>
        <a
          class="nav-link nav-link-otto w-nav-link"
          data-toggle="collapse"
          data-target=".navbar-collapse.show"
        >
          Log in
        </a>
      </li>

      <li class="nav-item header-margin" onClick={handleSignup}>
        <a
          class="nav-link button-navigation w-button header-signup"
          data-toggle="collapse"
          data-target=".navbar-collapse.show"
        >
          Sign up
        </a>
      </li>
    </ul>
  );

  const loggedInMenu = (
    <ul class="navbar-nav ml-auto flex-nowrap">
      <li class="nav-item header-margin" onClick={handleMe}>
        <a
          class="nav-link nav-link-otto w-nav-link"
          data-toggle="collapse"
          data-target=".navbar-collapse.show"
        >
          Me
        </a>
      </li>

      <li class="nav-item header-margin d-none d-lg-block" onClick={myBookings}>
        <a
          class="nav-link nav-link-otto w-nav-link"
          data-toggle="collapse"
          data-target=".navbar-collapse.show"
        >
          Account
        </a>
      </li>

      <li class="nav-item header-margin d-lg-none" onClick={myBookings}>
        <a
          class="nav-link nav-link-otto w-nav-link"
          data-toggle="collapse"
          data-target=".navbar-collapse.show"
        >
          Bookings
        </a>
      </li>
      <li
        class="nav-item header-margin d-lg-none"
        onClick={handleEditBasicProfile}
      >
        <a
          class="nav-link nav-link-otto w-nav-link"
          data-toggle="collapse"
          data-target=".navbar-collapse.show"
        >
          Edit Profile
        </a>
      </li>
      <li
        class="nav-item header-margin d-lg-none"
        onClick={handleEditAvailability}
      >
        <a
          class="nav-link nav-link-otto w-nav-link"
          data-toggle="collapse"
          data-target=".navbar-collapse.show"
        >
          Availability
        </a>
      </li>
      <li
        class="nav-item header-margin d-lg-none"
        onClick={handleEditAvailableTasks}
      >
        <a
          class="nav-link nav-link-otto w-nav-link"
          data-toggle="collapse"
          data-target=".navbar-collapse.show"
        >
          Meetings
        </a>
      </li>
      <li class="nav-item header-margin" onClick={logout}>
        <a
          class="nav-link nav-link-otto w-nav-link"
          data-toggle="collapse"
          data-target=".navbar-collapse.show"
        >
          Log out
        </a>
      </li>
    </ul>
  );

  let profile_url = "/p/" + authContext.shortUsername;

  let menu_contents = "";

  if (authContext.authInitialized && authContext.isLoggedIn) {
    menu_contents = loggedInMenu;
  } else if (authContext.authInitialized && !authContext.isLoggedIn) {
    menu_contents = loggedOutMenu;
  } else {
    // This is just so we don't do a flippy-do when we first load up the page.
    menu_contents = <div></div>;
  }

  // ********************************************************
  // TODO: link these to pages.
  // TODO: figure out if it's actually signed in.
  return (
    <div class="pb-4" style={{ backgroundColor: headerBackgroundColor }}>
      <div class="webflow-container">
        <nav
          class="navbar navbar-expand-lg navbar-light"
          style={{
            backgroundColor: headerBackgroundColor,
          }}
        >
          <div class="d-flex flex-grow-1">
            <a class="navbar-brand" href="/">
              <span class="brand-logo">BOOKTIME</span>
            </a>

            <div class="w-100 text-right">
              <button
                class="navbar-toggler"
                type="button"
                data-toggle="collapse"
                data-target="#navbarNavAltMarkup"
                aria-controls="navbarNavAltMarkup"
                aria-expanded="false"
                aria-label="Toggle navigation"
              >
                <span class="navbar-toggler-icon"></span>
              </button>
            </div>
          </div>

          <div
            class="collapse navbar-collapse flex-grow-1 text-right"
            id="navbarNavAltMarkup"
          >
            {menu_contents}
          </div>
        </nav>
      </div>
    </div>
  );
}

export default withRouter(OurHeader);
