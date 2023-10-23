// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import React from 'react';
import ReactDOM from 'react-dom/client';
import { Amplify } from 'aws-amplify';
import { Authenticator } from '@aws-amplify/ui-react';

import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';

import App from './App';
import awsExports from './aws-exports'; 
import reportWebVitals from './reportWebVitals';

Amplify.configure({
  Auth: {
    region: awsExports.region,
    userPoolId: awsExports.user_pool_id,
    userPoolWebClientId: awsExports.user_pool_client_id
  }
})

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Authenticator.Provider>
      <App />
    </Authenticator.Provider>
  </React.StrictMode>
);

reportWebVitals();
