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
        profilephoto: {
            // flexShrink: 0,
            "@media (max-width: 520px)": {
              margin: "0px",
              maxWidth: "100%",
              borderRadius: "7px",
            },
            "@media (min-width: 520px)": {
              objectFit: "cover",
              height: "400px",
              maxWidth: "100%",
              borderRadius: "7px",
            },
          },


    },
  }));


// This all might be too much work.
// A thing that represents a single dish.
function OneDish(props) {
    const classes = useStyles();
    const history = useHistory();

    // I don't think I have any... real things here.

    useEffect(() => {
        // Any init stuff, I guess.

    }, [])


    const onSelect = () => {

        // Redirects you to the checkout page for this dish.
        //console.log("Well, this was clicked, so you can actually... redirect now.")
    }

    let internal = '';
    // Easy thing.
    // photo,
    if (props.dish) {
        internal = (
            <div>
                <img className={classes.profilephoto}
                src={props.dish.main_photo}
                />
                <div>
                    {props.dish.name} ${props.dish.price}
                </div>

            </div>
        )
    }

    return (
        <div onClick={onSelect}>
            {internal}
        </div>
    )
}


// Basically, dishes should be arranged like this.
function DishArray(props) {

    const classes = useStyles();
    const history = useHistory();

    // Not super importante.
    useEffect(() => {
    }, []);

    console.log("Doin it inside DishArray, the dishes are ", props.dishes);

    let childDishes = '';
    if (props.dishes) {
        // We will

        childDishes = (
            <div>
                {
                    props.dishes.map((oneDish, index) => {
                        // Something simple.
                        return (
                            <OneDish dish={oneDish} key={index} />
                        )

                    })
                }

            </div>
        )
    }

    return (
        <div>
            {childDishes}
        </div>
    )


}

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

        let info_url = new URL(USING_URL + "/get_influencer_info");
        fetch(info_url, {
            method: "POST",
            body: userInfoForm,
        }).then((response) => {
            // ugh.
            if (response.status == 200) {
                response.json().then((data) => {
                    if (data.success) {
                        // Then we can set it...
                        setUserInfo(data.info_dict)
                        // Also, then we can start fetching their dishes?
                        console.log("We got their userInfo, ", data.info_dict);
                        fetch_dishes(influencer_username, zip_code);
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

    // Making this its own function because nesting all those fxns would make me
    // insane.
    const fetch_dishes = (influencer_username, zip_code) => {

        let dishesForm = new FormData();
        dishesForm.set("influencer_name", influencer_username);
        dishesForm.set("zip_code", zip_code);

        let dishes_url = new URL(USING_URL + "/get_influencer_dishes_area");
        fetch(dishes_url, {
            method: "POST",
            body: dishesForm,
        }).then((response) => {
            if (response.status == 200) {
                response.json().then((data) => {
                    if (data.success) {
                        // Then, we have the dishes.
                        console.log("We got their dishes", data.all_dishes);
                        setFaveDishes(data.all_dishes);
                    } else {
                        // bad
                    }
                }).catch((error) => {
                    // bad 2
                })
            } else {
                // bad 3.
            }
        })
    }

    let personal_section = '';

    // Only two things are:
    //
    if (userInfo) {
        let photo_elt = (
            <img
                  className={classes.profilephoto}
                  src={userInfo.avatar_path}
                />
        )

        personal_section = (
            <div className="row justify-content-center">
            <div className="col-md-6 my-1">

            <div>
                {photo_elt}
            </div>

            <div>
                {userInfo.display_name}
            </div>
            <div>
                {userInfo.first_name} {userInfo.last_name}
            </div>



            </div>
            </div>
        )

    }
    // This is super stupid, but here is my profile.



    // This should be set after
    let dishes_section = '';
    if (faveDishes) {

        dishes_section = (<DishArray dishes={faveDishes} />)
    }



    return (

        <div>
        {personal_section}
        {dishes_section}
        </div>
      )


}

export default UserPage;