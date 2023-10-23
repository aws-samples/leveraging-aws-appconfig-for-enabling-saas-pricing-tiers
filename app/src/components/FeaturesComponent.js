// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import React from 'react';
import { Authenticator } from '@aws-amplify/ui-react';
import { Route, Routes } from 'react-router-dom';
import { Spinner } from 'react-bootstrap';

import '@aws-amplify/ui-react/styles.css';

import { useFeatures } from './FeaturesContext';
import { Analytics } from './features/Analytics';
import { CRM } from './features/CRM';
import { Email } from './features/Email';
import { Sidebar } from './Sidebar';


export const FeaturesComponent = () => {
    const { loading, fullname, tenant, tier } = useFeatures();

    return (
        <Authenticator hideSignUp="true">
            <div className="container">
                {loading ? (
                    <Spinner
                        animation="border"
                        role="status"
                        style={{ position: 'absolute', top: '50%', left: '50%' }}
                    >
                        <span className="visually-hidden">Loading...</span>
                    </Spinner>
                ) : (
                    <>
                        <div className="sidebar-container">
                            <Sidebar />
                        </div>
                        <div className="content-container">
                            <div className="title-container">
                                <h5 className="title">Logged in as <strong>{fullname}</strong></h5>
                                <div className="tier-info">Your company name: <strong>{tenant}</strong></div>
                                <div className="tier-info">Your subscription plan: <strong>{tier}</strong></div>
                            </div>
                            <div className="content-divider"></div>  {/* Divider */}
                            <div className="page-content">
                                <Routes>
                                    <Route path="/analytics" element={<Analytics />} />
                                    <Route path="/crm" element={<CRM />} />
                                    <Route path="/email" element={<Email />} />
                                </Routes>
                            </div>
                        </div>
                    </>
                )}
            </div>
        </Authenticator>
    );      
};

