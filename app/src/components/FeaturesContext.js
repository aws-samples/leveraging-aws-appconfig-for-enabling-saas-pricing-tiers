// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import React, { useState, useEffect, createContext, useContext } from 'react';
import axios from 'axios';
import { Auth } from 'aws-amplify';
import { useAuthenticator } from '@aws-amplify/ui-react';

import awsExports from "../aws-exports";

const FeaturesContext = createContext();

export const useFeatures = () => {
    return useContext(FeaturesContext);
};

export const FeaturesProvider = ({ children }) => {
    const { authStatus } = useAuthenticator((context) => [context.user]);
    const [features, setFeatures] = useState([]);
    const [loading, setLoading] = useState(true);
    const [fullname, setFullname] = useState('');
    const [tenant, setTenant] = useState('');
    const [tier, setTier] = useState('');

    useEffect(() => {
        async function fetchFeatures() {
            try {
                const session = await Auth.currentSession();
                const idToken = session.getIdToken().getJwtToken();

                const response = await axios.get(`${awsExports.api_gateway.regional_endpoint}features`, {
                    headers: {
                        Authorization: 'Bearer ' + idToken
                    }
                });

                if (response.data) {
                    console.log(response.data)
                    setFeatures(response.data.features);
                    setFullname(response.data.fullname);
                    setTenant(response.data.tenant);
                    setTier(response.data.tier);
                }
            } catch (error) {
                console.error("Error fetching features:", error);
            }

            setLoading(false);
        }

        if (authStatus === 'authenticated') { fetchFeatures(); }
    }, [authStatus]);

    const value = {
        features,
        loading,
        fullname,
        tenant,
        tier
    };

    return (
        <FeaturesContext.Provider value={value}>
            {children}
        </FeaturesContext.Provider>
    );
};
