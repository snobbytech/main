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

import StripePay from "./StripePay";

import StarIcon from '@material-ui/icons/Star';
import * as Sentry from "@sentry/react";
import qs from 'qs';

const { Title, Text, Link } = Typography;
const { TextArea } = Input;

var USING_URL = process.env.REACT_APP_BACKEND_URL;

const useStyles = makeStyles((theme) => ({
    ...universal_styles,
    ...{
        dishname: {
            fontFamily: "Quicksand",
            fontStyle: "normal",
            fontWeight: "bold",
            fontSize: "16px",
            lineHeight: "24px",
            display: "flex",
            alignItems: "center",
            letterSpacing: "-0.0041em",

            color: "#111827",
        },

        dishphoto: {
            width:"100%",
            objectFit: "cover",
            borderRadius: "8px",
          },

          deliveryrestaurantheader: {
            textAlign: "center",
            fontFamily: "Quicksand, sans-serif",
            fontStyle: "normal",
            fontWeight: "bold",
            fontSize: "16px",
            lineHeight: "20px",
            letterSpacing: "-0.0041em",
            color: "#111827",

          },

          deliveryrestaurantaddress: {
            textAlign: "center",
            fontFamily: "Quicksand, sans-serif",
            fontStyle: "normal",
            fontSize: "12px",
            letterSpacing: "-0.0041em",
            color: "#111827",
          },

          orderprice: {
            fontFamily: "SF Pro Display",
            fontStyle: "normal",
            fontWeight: "600",
            fontSize: "14px",
            lineHeight: "17px",
            /* identical to box height */
            letterSpacing: "-0.0041em",
            color: "#EDBC0E",
          },

          tip: {
            display: "inline-block",
            width: "80px",
            backgroundColor: "white",

            /*  border: 1px solid #d6d6d6; */
            border: "1px solid #E8E8E8",
            borderRadius: "8px",
            marginLeft: "5px",
            marginRight: "5px",
            padding: "15px",
            cursor: "pointer",
          },

          tipselected: {
            display: "inline-block",
            width: "80px",
            backgroundColor: "#FFFC00",
            borderRadius: "5px",
            marginLeft: "5px",
            marginRight: "5px",
            padding: "15px",
            cursor: "pointer",
          },

          tipcontent: {
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            /* Added this line for cases where the package description cell-wraps.  */
            textAlign: "center",

            fontFamily: "Source Sans Pro",
            fontStyle: "normal",
            fontWeight: "500",
            fontSize: "12px",
            lineHeight: "18px",
            color: "#151E34",
          },

          tippercent: {
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            /* Added this line for cases where the package description cell-wraps.  */
            textAlign: "center",


            fontFamily: "Source Sans Pro",
            fontStyle: "normal",
            fontWeight: "600",
            fontSize: "16px",
            lineHeight: "18px",
            color: "#151E34",

          },


          pricelineitem: {
            fontFamily: "Source Sans Pro",
            fontStyle: "normal",
            fontWeight: "500",
            fontSize: "14px",
            lineHeight: "20px",
            /* identical to box height, or 143% */
            color: "#151E34",
          },

          pricelinevalue: {
            fontFamily: "Source Sans Pro",
            fontStyle: "normal",
            fontWeight: "500",
            fontSize: "16px",
            lineHeight: "20px",
            /* identical to box height, or 125% */

            textAlign: "right",

            color: "#151E34",
          },

          totallabel: {
            fontFamily: "Source Sans Pro",
            fontStyle: "normal",
            fontWeight: "600",
            fontSize: "14px",
            lineHeight: "20px",
            /* identical to box height, or 143% */
            color: "#151E34",
          },

          totalprice: {
            fontFamily: "Source Sans Pro",
            fontStyle: "normal",
            fontWeight: "bold",
            fontSize: "16px",
            lineHeight: "20px",
            textAlign: "right",
            color: "#151E34",
          },

          payamountdivs: {
            /* Not showing the background color as in the mock, because part of the layout looks bad here*/
          }

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
    const [restaurantInfo, setRestaurantInfo] = useState({});
    // Contains and explains all the partial charges we'll have in order
    // placement.
    const [preOrderInfo, setPreOrderInfo] = useState({});

    // When we update the preOrderInfo, we'll have to also update the stripeSecret.
    const [stripeSecret, setStripeSecret] = useState("");


    // Hmm,
    const [address, setAddress] = useState({});


    // Probably/maybe will have some issues here.
    const [err, setErr] = useState("");

    useEffect(() => {
        // At the start of the flow, we talk to the server and get info for the dish.

        // OK, so what is the dish?
        let qss = qs.parse(window.location.search, {ignoreQueryPrefix: true});
        let dish_id = qss.dish_id;

        let dish_data = new FormData();
        dish_data.set("dish_id", dish_id);
        // TODO: read this in from memory or something.
        dish_data.set("source_influencer", "");


        // Grab both the dish and calculate its payment info.
        let preorder_url = new URL(USING_URL + "/get_dish_order_details");
        fetch(preorder_url, {
            method: "POST",
            body: dish_data
        }).then((response) => {
            if (response.status == 200) {
                response.json().then((data) => {
                    if (data.success) {
                        // Then we can start grabbing the response types, yeah?
                        setDishInfo(data.dish_dict);
                        setPreOrderInfo(data.order_dict);
                        setRestaurantInfo(data.restaurant_dict);
                    }
                })
            }
        })


        // Okiedokie, now we ask the good people about both our dish and the order.

    }, [])

    useEffect(() => {
        setStripeSecret("");
        if (Object.keys(preOrderInfo).length > 0) {
            // Make a request to the backend
            // IMMEDIATE TODO: implement this.

            //fetchStripeSecret();
        }

    }, [preOrderInfo])


    const chooseTip= (tipAmt) => {
        // Set the tip amount, recalculate the total, and ask for the stripe secret again.
        // Also, set the chosenTip.

        let curPreOrder = {...preOrderInfo};
        curPreOrder.tip = Number(tipAmt);
        curPreOrder.total_cost = curPreOrder.subtotal + curPreOrder.delivery_fee + curPreOrder.local_tax + curPreOrder.tip;
        setPreOrderInfo(curPreOrder);
    }

    // Make sure that the address is correct and that we can deliver.
    const validateAddress = () => {

    }


    // Not implementing this yet, but o well.
    const submitOrder = () => {

    }

    //
    const fetchStripeSecret = () => {

    }


    let restaurantSection = '';
    if (Object.keys(restaurantInfo).length) {
        //
        restaurantSection = (
            <div className=" mt-3">

            <div className="row justify-content-center">
                <div className={ classes.deliveryrestaurantheader + " col-md-6 col-9 "}>
                    Delivery from {restaurantInfo.name}
                </div>
            </div>

            <div className="row justify-content-center">
                <div className={classes.deliveryrestaurantaddress + " col-md-6 col-9"}>
                    {restaurantInfo.street_address + " | " + restaurantInfo.phone}
                </div>
            </div>
        </div>
        )
    }


    let dishSection = '';
    if (Object.keys(dishInfo).length && Object.keys(restaurantInfo).length) {
        // Then we can create some divs and stuff.
        dishSection = (
            <div className="row mt-4 ">
            <div className="col-md-4 col-4">
                <img className={classes.dishphoto}
                    src={dishInfo.main_photo}
                />
            </div>

            <div className="col-md-8 col-8">
                <div className={classes.dishname}>
                    {dishInfo.name}
                </div>
                <div className={""}>
                    <span className={classes.orderprice}>${dishInfo.price}</span>
                </div>

            </div>

            </div>
        )


    }


    // This is the top part.
    let checkoutSection = '';
    if (dishInfo &&  preOrderInfo) {
        checkoutSection = (
            <div>

            </div>

        )
    }


    // Big ole stuff.
    // Address
    // Name
    // Street address
    // phone number
    let addressForm = (
        <div className="">
            <Form>
            <div className="row">
                <div className="col-10">
                  <Form.Group controlId="name">
                  <Form.Label>Name</Form.Label>
                    <Form.Control
                    placeholder="Your Name"
                    controlId="name"
                    />
                </Form.Group>
              </div>

            </div>
            <div className="row">
                <div className="col-md-6 col-10">

            <Form.Group controlId="streetaddress">
              <Form.Label>Street Address</Form.Label>
                <Form.Control
                  placeholder="Full Street Address"
                  controlId="streetaddress"
                />
            </Form.Group>
            </div>
            </div>

            <div className="row">
            <div className="col-md-2 col-4">

            <Form.Group controlId="aptnumber">
              <Form.Label>Unit no.</Form.Label>
                <Form.Control
                  placeholder="Unit #"
                  controlId="aptnumber"
                />
            </Form.Group>

            </div>
            </div>


            <div className="row">
                <div className="col-md-6 col-10">

            <Form.Group controlId="city">
              <Form.Label>City</Form.Label>
                <Form.Control
                  placeholder="City"
                  controlId="city"
                />
            </Form.Group>

            </div>
            </div>

            <div className="row">
            <div className="col-md-2 col-4">

            <Form.Group controlId="state">
              <Form.Label>State</Form.Label>
                <Form.Control
                  placeholder="State"
                  controlId="state"
                />
            </Form.Group>

            </div>

            </div>

            <div className="row">
            <div className="col-md-4 col-4">
            <Form.Group controlId="zip">
              <Form.Label>Zip</Form.Label>
                <Form.Control
                  placeholder="Zip Code"
                  controlId="zip"
                />
            </Form.Group>
            </div>

            </div>


            <div className="row">
            <div className="col-md-2 col-10">


            <Form.Group controlId="phone">
              <Form.Label>Phone Number</Form.Label>
                <Form.Control
                  placeholder="Phone number"
                  controlId="phone"
                />
            </Form.Group>
            </div>
            </div>

            </Form>
        </div>
    )

    // Delivery instructions.
    // Keeping this simple for now, because it's going to be easier to
    // drop-off-location
    // notify me?
    // This is
    let deliveryInstructionsForm = (
        <div className="">

            <Form>
            <div className="row">
                <div className="col-10">

            <Form.Group controlId="phone">
              <Form.Label>Delivery Instructions</Form.Label>
                <Form.Control
                  placeholder="(eg. Leave it at the front door and call/text me)"
                  controlId="delivery_instructions"
                />
            </Form.Group>
            </div>
            </div>

            </Form>
        </div>

    )

    // This is like... the stripe form.

    // To make it easy, I should suggest a 18% tip amount.

    let payForm = '';
    console.log("From outside: I have length ", Object.keys(preOrderInfo).length);
    if (Object.keys(preOrderInfo).length) {
        console.log("Hi, I am inside the computer");
        let stripe_block = (
            <div>
              <StripePay
                validateBeforePayment={() => {}}

                stripeSecret={stripeSecret}
              />
            </div>
        );

    // Goes through the preOrderInfo and makes a thing.
    let toPaySection = '';
    toPaySection = (
        <>

        <div className="row">
            <div className="col-md-10 col-10">Food total</div>
            <div className="col-md-2 col-2">${preOrderInfo.subtotal}</div>
        </div>
        <div className="row">
            <div className="col-md-10 col-10">Tax</div>
            <div className="col-md-2 col-2">${preOrderInfo.local_tax}</div>
        </div>
        <div className="row">
            <div className="col-md-10 col-10">Delivery Fee</div>
            <div className="col-md-2 col-2">${preOrderInfo.delivery_fee}</div>
        </div>
        </>
    )


    // Make a tip portion.

    // OK, this is really stupid to hardcode but I guess here I am.
    let notip       = 0;
    let fifteenperc = (preOrderInfo.subtotal * 0.15).toFixed(2);
    let eighteenperc = (preOrderInfo.subtotal * 0.18).toFixed(2);

      let noselectedclass = classes.tip;
      let fifteenselectedclass = classes.tip;
      let eighteenpercclass = classes.tip;
      if (preOrderInfo.tip == notip) {
        noselectedclass = classes.tipselected;
      }
      if (preOrderInfo.tip == fifteenperc) {
        fifteenselectedclass = classes.tipselected;
      }
      if (preOrderInfo.tip == eighteenperc) {
        eighteenpercclass = classes.tipselected;
      }

          let tipPortion = (
          <div className="row mb-3">
                <div
                    className={  noselectedclass + " ml-2 mr-2 mt-1"}
                    onClick={() => {
                      chooseTip(notip);
                    }}
                  >
                    <div className={classes.tippercent}>
                      No tip
                    </div>
                  </div>

                  <div
                    className={  fifteenselectedclass + " ml-2 mr-2 mt-1"}
                    onClick={() => {
                      chooseTip(fifteenperc);
                    }}
                  >
                    <div className={classes.tippercent}>
                      15%
                    </div>
                    <div className={classes.tipcontent}>
                    ${fifteenperc}
                    </div>
                  </div>

                  <div
                    className={  eighteenpercclass + " ml-2 mr-2 mt-1"}
                    onClick={() => {
                      chooseTip(eighteenperc);
                    }}
                  >
                    <div className={classes.tippercent}>
                      18%
                    </div>
                    <div className={classes.tipcontent}>
                    ${eighteenperc}
                    </div>
                  </div>
        </div>
    )


    payForm = (
        <div className="">
            {tipPortion}

            <div className={classes.payamountdivs }>
            {toPaySection}

            <div className="row">
            <div className={classes.totallabel + " col-md-10 col-10"}>Total</div>
            <div className={classes.totalprice + " col-md-2 col-2"}>{preOrderInfo.total_cost}</div>
            </div>
            </div>

            {stripe_block}

        </div>
    )
    }

    console.log("Payform is like", payForm);

    // The stripe stuff should include the pay button as well.


    // This is... just going to be a big ole form.

    return (
        <div className="container">

            {restaurantSection}
            {dishSection}
            <div className="mt-4" >

            <hr />
            </div>

            {addressForm}
            {deliveryInstructionsForm}

            {payForm}
        </div>
    )
}

export default StartCheckout;