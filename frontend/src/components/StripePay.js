// OK, this is the element that does the actual cc
import React, { useState, useContext, useEffect, useRef } from "react";
import { makeStyles } from "@material-ui/styles";
import universal_styles from "./UniversalStyles";
import { Typography } from 'antd';
import { Elements } from '@stripe/react-stripe-js';
import { loadStripe } from '@stripe/stripe-js';
import { Input } from 'antd';
import { Spin } from "antd";
import amplitude from "amplitude-js";
import * as Sentry from "@sentry/react";

import { useStripe, useElements, CardElement } from '@stripe/react-stripe-js';
const { Title, Text, Link } = Typography;

let USING_URL = process.env.REACT_APP_BACKEND_URL;

// stripePromise should not be kept here because we apparently need to
// include the accountID when loading stripe.  Come on guys!
//let stripePromise = '';
let stripeKey = ''
if (USING_URL == '') {
  // live pk.
  //  stripePromise = loadStripe("pk_live_9fy0PE9aTVxyV6k4oS0UTQa2005sATcOwW");
  stripeKey = "pk_live_51HtkfVI5P0GyTyGvMMwCIGd4SWDSbb1UsKEbGRdXYHNu1Tg3N6lti4fxyUj6Lx97uzayEI2ZsBOGYkOn2BDWfZPP00mGWVSP6m";
} else {
  // test pk.
  //  stripePromise = loadStripe("pk_test_51HtkfVI5P0GyTyGvP1Rjs4E3t5TLaVcyyyETdwFYZjYAckYy2g7HUvh6gVtEgy59yAHLm48Gz4XVCo4YMuox9mQo00PqXGafqr");
  stripeKey = "pk_test_51HtkfVI5P0GyTyGvP1Rjs4E3t5TLaVcyyyETdwFYZjYAckYy2g7HUvh6gVtEgy59yAHLm48Gz4XVCo4YMuox9mQo00PqXGafqr";
}

// Pretty much copying the stuff from StripePay.js, but now we'll be
// taking in actual amounts
const CARD_ELEMENT_OPTIONS = {
  style: {
    base: {
      color: "#424770",
      fontFamily: "Source Code Pro, monospace",
      fontSmoothing: "antialiased",
      fontSize: "16px",
      "::placeholder": {
        color: "#aab7c4",
      },
    },
    invalid: {
      color: "#fa755a",
      iconColor: "#fa755a",
    },
  },
};

function CardSection() {
  return (
    <div className="">

      <label>
        Payment Info
        </label>
      <div className="bounded-box p-2">
        <CardElement options={CARD_ELEMENT_OPTIONS} />
      </div>
    </div>
  );
};


// A whole thing to do stripe payment
function CheckoutForm(props) {
  const stripe = useStripe();
  const elements = useElements();

  // After we make the initial order request, we should get an id that lets us know
  // which order it is that we're trying to handle.
  const orderId = useRef('');

  const [paymentDone, setPaymentDone] = useState(false);
  const [currentlyPaying, setCurrentlyPaying] = useState(false);

  // for stripe-specific errors.
  const [error, setError] = useState("");

  useEffect(() => {
  }, []);

  // TODO:
  const makePaymentCall = async (formResponses) => {
    // Make a call to the backend that tells us the details of an order.
    let myForm = new FormData();

    // TODO: make these fields map to the details of an Order class.
    // Should also have to do with a restaurant and stuff.


    //console.log("About to make the booking post from the front end");

    let update_transaction_url = new URL(USING_URL + '/');
    await fetch(update_transaction_url, {
      method: 'POST',
      body: myForm
    }).then(async (response) => {
      if (response.status == 200) {
        await response.json().then((data) => {
          //console.log('In full, our data looks like ', data);
          if (data.success) {
            // In this case, I should record the orderId
            orderId.current = data.order_id;
            return true;
          }
        })
      }
    })
  }

  const handlePayment = async (event) => {
    // We don't want to let default form submission happen here,
    // which would refresh the page.
    event.preventDefault();

    // Reset error when we make a new payment.
    setError("");

    // Start the spinner
    setCurrentlyPaying(true);

    // We first ask the parent to do a validation, before we pay.
    let form_responses = props.validateBeforePayment();


    //console.log('We are in the stripe process now. We are checking the form responses: ', form_responses);
    if (!form_responses.success) {
      // This means there was some validation problem in the data.
      // Otherwise, we should have a form with "name" and "email" fields.
      setCurrentlyPaying(false);
      return;
    }

    // Here: make a booking over to the backend. Wait for it to end.
    await makePaymentCall(form_responses);

    if (!orderId.current) {
      setError("An error happened when talking to our server. You didn't get charged. We're on this, but also feel free to reach out to us");
      setCurrentlyPaying(false);
      return;
    }

    if (!stripe || !elements) {
      // Stripe.js has not yet loaded.
      // Make sure to disable form submission until Stripe.js has loaded.
      setCurrentlyPaying(false);
      return;
    }

    // Let's grab their name and email here too.
    const result = await stripe.confirmCardPayment(props.stripeSecret, {
      payment_method: {
        card: elements.getElement(CardElement),
        billing_details: {
          name: 'Some name',
        },
      }
    });

    if (result.error) {
      // Show error to your customer (e.g., insufficient funds)
      if (result.error.message) {
        setError("Payment processer had an issue: " + result.error.message + " if this persists, please contact the site admin at the email below.");
       // Sentry.captureMessage("We ran into a error in finalizing stripe payment. The message was: " + result.error.message);
      }
      setCurrentlyPaying(false);
    } else {
      // The payment has been processed!
      if (result.paymentIntent.status === 'succeeded') {
        // Show a success message to your customer
        // There's a risk of the customer closing the window before callback
        // execution. Set up a webhook or plugin to listen for the
        // payment_intent.succeeded event that handles any business critical
        // post-payment actions.


        // update the backend about this transaction.
        let myForm = new FormData();
        // set all the ishes.
        // I need to actually get this set up.

        myForm.set('order_id', orderId.current);

        let update_transaction_url = new URL(USING_URL + '/mark_order_paid');
        fetch(update_transaction_url, {
          method: 'POST',
          body: myForm
        }).then((response) => {
          if (response.status == 200) {
            response.json().then((data) => {
              if (data.success) {
                // Everything is perfect. You are perfect.
                setPaymentDone(true);
                setCurrentlyPaying(false);
              } else {
                setError("We encountered a problem talking to our own server. It has been reported, but feel free to reach out to us too.");
                //Sentry.captureMessage("We ran into a error in finalizing a booking, after . The message was: " + result.error.message);
                setCurrentlyPaying(false);
              }
            })
          }

        })
      }
    }
  };

  let spinner_or_button =  (
    <button className="btn btn-primary " disabled={!stripe}>Confirm order</button>
  );
  if (currentlyPaying) {
    spinner_or_button = (
      <div>
          <Spin size="large" /> <span className="mx-2">Finalizing booking</span>
      </div>
    )
  }


// Really, if the order went through, we should be redirecting them to the order status page.
// TODO: implement this.
  if (paymentDone) {
    return (
      <div className="py-2 px-2">
        <div>
          <Title level={3}>Success!</Title>
        </div>
        <div>
          Your order went through. You'll find a confirmation in your inbox.
        </div>
      </div>
      )
  }

  // TODO:
  // Add something here that tells them how much they're paying,
  // and asks for their name and email.
  return (
    <div>

      <div className="stripe-checkout-form py-3">
        <form onSubmit={handlePayment}>
          <CardSection />
          <div className="container-fluid px-0 my-3">
            <div className="row">
              <div className="col col-sm-12 col-md-6 col-lg-6">
              {spinner_or_button}
            </div>
          </div>
          </div>
          <div className="my-2 error_text">{error}</div>
        </form>
      </div>
    </div>

  );

}

function StripePay(props) {

  useEffect(() => {

  }, []);

  let ccline = '';
  // THIS IS TERRIBLE CHECKING
  // TODO: CHANGE THIS.
  if (USING_URL != 'https://booktimeserver.xyz') {
    ccline = ' By the way the test cc number is 4000 0025 0000 3155';
  }

  return (
    <div className="container px-0">
      <div className="row no-gutters">
        <div className="col col-lg-8 col-md-12 col-sm-12" >
          <div className="mt-2 slightly-larger ">
            <div className="flexy-spreadout">
            </div>
            <br />
            {ccline}
          </div>
        </div>
      </div>

      <div className="row no-gutters">
        <div className="col col-lg-8 col-md-8 col-sm-12" >
          <Elements stripe={loadStripe(stripeKey, { stripeAccount: props.stripe_id })}>
            <CheckoutForm validateBeforePayment={props.validateBeforePayment} stripeSecret={props.stripeSecret} orderInfo={props.orderInfo}  />
          </Elements>
        </div>
      </div>
    </div>
  )

};

export default StripePay;