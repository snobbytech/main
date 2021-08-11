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
import MailIcon from "@material-ui/icons/Mail";
import AccessTimeIcon from "@material-ui/icons/AccessTime";
import { Tooltip } from "antd";
import HelpOutline from "@material-ui/icons/HelpOutline";
import { withRouter, useHistory } from "react-router-dom";
import { Rate } from 'antd';
import { Form, FormFile } from "react-bootstrap";

import {Converter} from 'showdown';

import StarIcon from '@material-ui/icons/Star';
import * as Sentry from "@sentry/react";
import qs from 'qs';

const { Title, Text, Link } = Typography;
const { TextArea } = Input;

var USING_URL = process.env.REACT_APP_BACKEND_URL;

const useStyles = makeStyles((theme) => ({
    ...universal_styles,
    ...{

    }
    }));

/*
    View that represents a checkout process. This is a pretty simple form, but
    oh well.

    I'm going to have it be just one dish right now, which should make it easier.

*/

// Let's just make a big form, huh.

function StartCheckout(props) {

    const classes = useStyles();
    const history = useHistory();

    const [dishInfo, setDishInfo] = useState({});
    // Contains and explains all the partial charges we'll have in order
    // placement.
    const [preOrderInfo, setPreOrderInfo] = useState({});

    const [address, setAddress] = useState({});

    // This is the part where we have to ask the backend how much the
    // freaking thing was.
    const [subtotal, setSubtotal] = useState({});


    // Probably/maybe will have some issues here.
    const [err, setErr] = useState("");

    useEffect(() => {
        return;
        // At the start of the flow, we talk to the server and get info for the dish.

        // OK, so what is the dish?
        let qss = qs.parse(window.location.search, {ignoreQueryPrefix: true});
        let dish_id = qss.dish_id;

        let dish_data = new FormData();
        dish_data.set("dish_id", dish_id);

        // Grab both the dish and calculate its payment info.
        let preorder_url = new URL(USING_URL + "/get_preorder_dict");
        fetch(preorder_url, {
            method: "POST",
            body: dish_data
        }).then((response) => {
            if (response.status == 200) {
                response.json().then((data) => {
                    if (data.success) {
                        // Then we can start grabbing the response types, yeah?
                        //setDishInfo(data.dish_info);
                        //setDishOrderInfo(data.preorder_info);
                    }
                })
            }
        })


        // Okiedokie, now we ask the good people about both our dish and the order.

    }, [])

    // Make sure that the address is correct and that we can deliver.
    const validateAddress = () => {

    }


    // Not implementing this yet, but
    const submitOrder = () => {

    }


    // This is the top part.
    let checkoutInfo = '';
    if (dishInfo &&  preOrderInfo) {
        checkoutInfo = (
            <div>
                This can be a thing.

            </div>

        )
    }


    // Big ole stuff.
    // Address
    // Name
    // Street address
    // phone number
    let addressForm = (
        <div>
            <Form>
              <Form.Group controlId="name">
              <Form.Label>Name</Form.Label>
                <Form.Control
                  placeholder="Your Name"
                  controlId="name"
                />
            </Form.Group>

            <Form.Group controlId="street address">
              <Form.Label>Street Address</Form.Label>
                <Form.Control
                  placeholder="Full Street Address"
                  controlId="streetaddress"
                />
            </Form.Group>

            <Form.Group controlId="phone">
              <Form.Label>Phone Number</Form.Label>
                <Form.Control
                  placeholder="Phone number"
                  controlId="phone"
                />
            </Form.Group>
            </Form>
        </div>
    )

    // Delivery instructions.
    // Keeping this simple for now, because it's going to be easier to
    // drop-off-location
    // notify me?
    // This is
    let deliveryInstructionsForm = (
        <div>

            <Form>

            <Form.Group controlId="phone">
              <Form.Label>Delivery Instructions</Form.Label>
                <Form.Control
                  placeholder="(eg. Leave it at the front door and call/text me)"
                  controlId="delivery_instructions"
                />
            </Form.Group>

            </Form>
        </div>

    )


    // This is like... the stripe form.

    // To make it easy, I should suggest a 18% tip amount.


    let payForm = '';
    payForm = (
        <div>
            Stripe stuff here.
            <Form>

            <Form.Group controlId="phone">
              <Form.Label>Tip</Form.Label>
                <Form.Control
                  placeholder={"18% = " + " $3.20"}
                  controlId="tip"
                />
            </Form.Group>
            Other Stripe stuff.

            </Form>

        </div>
    )


    // The stripe stuff should include the pay button as well.


    // This is... just going to be a big ole form.

    return (
        <div>

            {checkoutInfo}
            {addressForm}
            {deliveryInstructionsForm}
            {payForm}
        </div>
    )
}

export default StartCheckout;