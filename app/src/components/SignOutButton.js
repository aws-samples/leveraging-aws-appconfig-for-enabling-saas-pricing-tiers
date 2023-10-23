// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { Button } from 'react-bootstrap';
import { useNavigate } from "react-router-dom";

import { Auth } from "aws-amplify";

export const SignOutButton = () => {
  const navigate = useNavigate();

  const onButtonClick = async () => {
    await Auth.signOut();
    alert("Signed out");
    navigate("/features");
  };

  return <Button className="sign-out-button" onClick={onButtonClick}>Sign Out</Button>;
};
