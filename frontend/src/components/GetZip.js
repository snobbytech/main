import React, { useState, useContext, useRef, useEffect } from "react";

import {
    Button,
    Form,
    Typography,
    Input,
    InputNumber,
    Select,
    Space,
    Spin,
    Tooltip,
  } from "antd";

import qs from 'qs';

import { withRouter, useHistory, useLocation } from "react-router-dom";

import { makeStyles } from "@material-ui/styles";

/*
    First page: grab the zipcode of the person and
*/

const useStyles = makeStyles({

    btn_container: {
      display: "flex",
      justifyContent: "flex-end",
    },

    doneBtn: {
      fontFamily: 'Poppins, sans-serif',
      fontStyle: "normal",
      fontWeight: "normal",
      fontSize: "16px",
      lineHeight: "24px",
      /* identical to box height */
      letterSpacing: "-0.0041em",
      /* Gray/300 */
      color: "#8C93A6",
      cursor: 'pointer',
      "&:hover": {
        color: "#454953",
      },

    },

    zip_text: {
      fontFamily: "Quicksand, sans-serif",
      fontStyle: "normal",
      fontWeight: "bold",
      fontSize: "28px",
      lineHeight: "40px",
      /* identical to box height, or 143% */

/*      display: flex;
      align-items: center;
      */
      letterSpacing: "-0.0041em",

      color: "#151E34",
    },

    zip_input: {
      height: "50px",
      /* Making this 100% because it's contained in a column that does sizing better.*/
      width: "100%",

      /* Yellow primary */

      border: "2px solid #FFE600",
      boxSizing: "border-box",
      borderRadius: "15px",

      "&:focus": {
        backgroundColor: "#f0f1f3",
        outline: 'none',

      },

    }

})

function GetZip(props) {
    const [err, setErr] = useState("");
    const history = useHistory();
    const classes = useStyles();

    // Pretty simple thing, right.

    const tryZip = (keyEvent) => {
        if (keyEvent.key == "Enter") {
            onSearchZip();
        }
    }

    const onSearchZip = () => {
        // Pretty simple, just check the backend.
        setErr("");

        // Get the value.
        let zipcode = document.getElementById('zipcode_input').value.trim();

        // Construct and set the window.

        // Make sure that it's a real zipcode?
        if (zipcode.length != 5) {
            // There's an error.
            setErr("The zipcode given, ", zipcode, " is the wrong length");
            return;
        }

        // Actually... at this point, let's just redirect to the influencer.
        let refer_name='';
        // Figure this arg out from our url args.
        let qss = qs.parse(window.location.search, {ignoreQueryPrefix: true});
        refer_name = qss.refer_name;

        if (!refer_name) {
            // OK, let's just assume an influencer. Someone like fionaeats.
            refer_name = 'fionaeats365';
            console.log("Didnt have a real referrer, so we set fiona by default");
        }

        console.log("About to redirect to", refer_name);

        // Also store here: the original referrer was this person.
        localStorage.setItem("snob_refer", refer_name);

        // TODO: save the history.
        history.push({
            pathname: "/u/" + refer_name,
        });

    }


    let top_text = (
        <div className="row justify-content-center my-2">
        <div className={classes.zip_text + " col-md-8 col-9 my-1"}>
        Show dishes near...
    </div>
    </div>
    )

    let zip_bar = (
      <div>

    <div className="row justify-content-center">
        <div className="col-md-8 col-9 my-2">
          <input
            className={classes.zip_input + " pl-3"}
            id="zipcode_input"
            placeholder="Zip Code"
            onKeyUp={tryZip}
          />
        </div>
      </div>
      </div>

    )


    // TODO:
    // This is for the mobile version.
    // On the desktop version, we should put the done_button BELOW the search bar
    // and give it a hover effect.
    let done_button = (
      <div className={classes.btn_container + " mt-3 pr-3"}>
      <div
        className={classes.doneBtn + " "}
        onClick={onSearchZip}
      >
        Done{" "}
      </div>
    </div>
    )



    return (
        <div>
        {done_button}
        {top_text}
        {zip_bar}
        </div>



    )

}


export default GetZip;