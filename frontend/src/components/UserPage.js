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
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
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
        coverphotocontainer: {
        },
        coverphoto: {
            height: "243px",
            width:"100%",
            objectFit: "cover",
        },

        profilephotocontainer: {
            marginTop: "-75px",
            textAlign: "center",
        },

        profilephoto: {
            // flexShrink: 0,
            border: "2px solid white",
            borderRadius: "50%",
            height: "150px",
          },

          profilefullname: {
              textAlign: "center",
              fontFamily: "Quicksand, sans-serif",
              fontStyle: "normal",
              fontWeight: "bold",
              fontSize: "18px",
              lineHeight: "24px",
              letterSpacing: "-0.0041em",
              color: "#111827",
          },
          profilecheckmark: {
            fontSize: '16px',
            marginBottom: "2px",
          },

          profiledisplayname: {
            textAlign: "center",
            fontFamily: "Dancing Script",
            fontStyle: "normal",
            fontWeight: "normal",
            fontSize: "30px",
            lineHeight: "36px",
            letterSpacing: "-0.41px",
            color: "#111827",
          },

          dishcontainer: {
              /* These shenanigans are basically so I can fight with the bootstrap grid.. */
            paddingLeft: "15px",
            paddingRight: "5px",
          },

          dishphoto: {
            height: "200px",
            width:"100%",
            objectFit: "cover",
            borderRadius: "10px",
          },

        dishdescription: {
            display: "flex",
            textAlign: "center",
            fontFamily: "Quicksand, sans-serif",
            fontSize: "12px",
            letterSpacing: "-0.0041em",
            color: "#111827",


        },
        innerdishdescription: {
            width: "90%",
        }

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

        // I should also
        /*
        history.push({
            pathname: "/startcheckout?dish_id=" + props.dish.id,
        })
        */
       // This is honestly ridiculous. I hate react. I hate javascript people.
       window.location.href = "/startcheckout?dish_id=" + props.dish.id;

    }

    let internal = '';
    // Easy thing.
    // photo,
    if (props.dish) {
        return (
            <div onClick={onSelect} className={ "col-6 " + classes.dishcontainer + " my-1"}>
                <div className=" px-1">
                <img className={classes.dishphoto}
                src={props.dish.main_photo}
                />

                </div>
                <div className={classes.dishdescription}>
                <div className={classes.innerdishdescription}>
                    {props.dish.name}
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div >
        </div>
    )
}


// Basically, dishes should be arranged like this.
function DishArray(props) {

    const classes = useStyles();

    // Not super importante.
    useEffect(() => {
    }, []);

    console.log("Doin it inside DishArray, the dishes are ", props.dishes);
    let childDishes = '';
    if (props.dishes) {
        // We will

        childDishes = (
            <div className={ " row px-1"}>
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


        // Things can change if we end with a slash.
        let pathname = window.location.pathname;
        if (pathname.lastIndexOf("/")+1 == pathname.length) {
            pathname = pathname.substring(0, pathname.lastIndexOf("/"));
        }


        let influencer_username = pathname.substring(
            pathname.lastIndexOf("/") + 1
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
    let cover_photo = '';

    // Only two things are:
    //
    if (userInfo) {

        cover_photo = (
            <div className={classes.coverphotocontainer}>
            <img className={classes.coverphoto} src={userInfo.cover_path} />

            </div>
        )

        let photo_elt = (
            <img
                  className={classes.profilephoto}
                  src={userInfo.avatar_path}
                />
        )

        personal_section = (
            <div className="row justify-content-center">
            <div className="col-md-5 col-5 my-2">

            <div className={classes.profilephotocontainer}>
                {photo_elt}
            </div>

            <div className={classes.profilefullname} >
                {userInfo.first_name} {userInfo.last_name} <CheckCircleIcon htmlColor="#3B62EA" className={classes.profilecheckmark} style={{}}/>
            </div>

            <div className={classes.profiledisplayname}>
                {userInfo.display_name}
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
        {cover_photo}
        {personal_section}
        {dishes_section}
        </div>
      )


}

export default UserPage;