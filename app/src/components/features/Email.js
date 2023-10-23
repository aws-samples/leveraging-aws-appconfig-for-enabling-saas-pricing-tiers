// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import React from 'react';
import { Button } from 'react-bootstrap';

import { useFeatures } from '../FeaturesContext';

export const Email = () => {
  const { features } = useFeatures();

  if (features.includes('email')) {
    return (
      <div className="feature-wrapper enabled-feature">
        <h2 className="feature-heading">Email Marketing ✅</h2>
        <p className="feature-description">
          Craft, send, and analyze campaigns that resonate!
        </p>
      </div>
    );
  }

  return (
    <div className="feature-wrapper disabled-feature">
      <h2 className="feature-heading">Email Marketing ❌</h2>
      <p className="feature-description">
        Upgrade your subscription plan to access premium features 🚀
      </p>
      <Button className="upgrade-button" onClick={() => {
        alert("Redirecting to upgrade page...");
      }}>
        Upgrade Now
      </Button>
    </div>
  );
};
