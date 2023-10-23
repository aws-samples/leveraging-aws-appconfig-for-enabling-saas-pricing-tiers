// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';

import { NavbarComponent } from './components/NavbarComponent';
import { RegisterComponent } from './components/RegisterComponent';
import { FeaturesComponent } from './components/FeaturesComponent';
import { FeaturesProvider } from './components/FeaturesContext';

import './App.css';

function HomeRedirect() {
    let navigate = useNavigate();

    useEffect(() => {
        navigate('/register');
    }, [navigate]);

    return null;
}

export default function App() {
    return (
        <div className="App">
            <FeaturesProvider>
                <Router>
                    <NavbarComponent />
                    <Routes>
                        <Route path="/features/*" element={<FeaturesComponent />} />
                        <Route path="/" element={<HomeRedirect />} />
                        <Route path="/register" element={<RegisterComponent />} />
                    </Routes>
                </Router>
            </FeaturesProvider>
        </div>
    );
}
