import React, { useState, useEffect, useRef } from "react";
import { Typography } from "antd";
import { makeStyles } from "@material-ui/styles";
import universal_styles from "./UniversalStyles";
import { useMediaQuery } from "react-responsive";

import { Input } from "antd";
import { Button, Card, Alert } from "antd";
import {
  LinkOutlined,
  ThunderboltOutlined,
  PercentageOutlined,
} from "@ant-design/icons";
import amplitude from "amplitude-js";
import AccessTimeIcon from "@material-ui/icons/AccessTime";
import { Tooltip } from "antd";
import HelpOutline from "@material-ui/icons/HelpOutline";
import { withRouter, useHistory } from "react-router-dom";

import {Converter} from 'showdown';

import * as Sentry from "@sentry/react";

const { Title, Text, Link } = Typography;
const { TextArea } = Input;

var USING_URL = process.env.REACT_APP_BACKEND_URL;

/*

Basic page showing an influencer, their likes/stuff, and then the foods they promote.


*/

const useStyles = makeStyles((theme) => ({
    ...universal_styles,
    ...{

    },
  }));

function UserPage(props) {

    const classes = useStyles();
    const history = useHistory();

    const [err, setErr] = useState("");
    // Their zip code.
    const [usingZip, setUsingZip] = useState("");

    // Basic info on the influencer.
    const [userInfo, setUserInfo] = useState({});

    // Basic info on the influencer's favorite dishes.
    // Note: this could be uninitialized, so I want to be careful here.
    const [faveDishes, setFaveDishes] = useState([]);

    useEffect(() => {

        // Grab the username.
        // TODO: change this name.
        let influencer_username = window.location.pathname.substring(
            window.location.pathname.lastIndexOf("/") + 1
        );

        if (!influencer_username) {
            setErr("Did not find the correct username.");
            return;
        }

        // Otherwise, place a request to the backend to get the user's info, and
        // also all their datas.


        // Sure, why not.
        let zip_code = "10011";

        // First, set the user's basic info:
        let userInfoForm = new FormData();
        userInfoForm.set("influencer_username", influencer_username);

        let info_url = new URL(USING_URL + "/fetch_influencer_info");
        fetch(info_url, {
            method: "POST",
            body: userInfoForm,
        }).then((response) => {
            // ugh.
            if (response.status == 200) {
                response.json().then((data) => {
                    if (data.success) {
                        // Then we can set it...

                        // Also, then we can start fetching their dishes?
                    } else {
                        // Another error condition.
                    }
                }).catch((error) => {
                    // Other error handling.

                })
            } else {
                // Some error handling.

            }

        })


    }, [])



    // This should be set after
    let dishes_section = '';




    return (

        <div>

        Soylent green is not you or me.
        </div>
      )


}

export default UserPage;