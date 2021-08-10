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

    btn: {

    }

})

function GetZip(props) {
    const [err, setErr] = useState("");
    const history = useHistory();

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
        let zipcode = document.getElementById('zipcode_input').nodeValue.trim();

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


        // TODO: save the history.
        history.push({
            pathname: "/u/" + refer_name,
        });


    }


    let top_text = (
        <div className="row justify-content-center">
        <div className="col-md-6 my-1">
        Please enter your zip code to find nearby dishes.
    </div>
    </div>
    )

    let zip_bar = (
        <div className="row justify-content-center">
        <div className="col-md-6 my-1">
          <Input
            className={}
            id="zipcode_input"
            placeholder="Zip Code"
            onKeyUp={tryZip}
          />
        </div>
        <div className="col-md-2 my-1 ">
          <Button
            className={classes.btn + " "}
            type="primary"
            onClick={onSearchZip}
          >
            {" "}
            Search{" "}
          </Button>
        </div>
      </div>

    )



    return (
        <div>

        {top_text}
        {zip_bar}
        </div>



    )

}


export default GetZip;