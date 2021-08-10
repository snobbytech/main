import React, { useState, useContext, useEffect } from "react";

import { auth } from "../base";
import * as firebase from "firebase";

import { AuthContext } from "../App";
import { useHistory } from "react-router-dom";
import {
  Button,
  Form,
  Typography,
  Input,
  InputNumber,
  Select,
  Space,
  Alert,
  Tooltip,
  Upload,
} from "antd";

const { Title, Text, Link } = Typography;


/*

A component that lets the requester set a price and pay and book. They can negotiate back and forth about it though.



Ugh. All this is annoying. It's really just a thing that creates a one-off booking price, and goes into our
Stripe and calendar booking flows.


*/
