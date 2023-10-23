// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import React from 'react';
import { NavLink } from 'react-router-dom';

import '../App.css';

import { SignOutButton } from './SignOutButton';
import { useFeatures } from './FeaturesContext';

export const Sidebar = () => {
    const { features } = useFeatures();
    return (
        <div className="sidebar">
            <NavLink className={features.includes('analytics') ? 'enabled-feature' : 'disabled-feature'} to="/features/analytics">Analytics</NavLink>
            <NavLink className={features.includes('crm') ? 'enabled-feature' : 'disabled-feature'} to="/features/crm">CRM</NavLink>
            <NavLink className={features.includes('email') ? 'enabled-feature' : 'disabled-feature'} to="/features/email">Email Marketing</NavLink>
            <div className="sidebar-footer">
                <SignOutButton />
            </div>
        </div>
    );
}
