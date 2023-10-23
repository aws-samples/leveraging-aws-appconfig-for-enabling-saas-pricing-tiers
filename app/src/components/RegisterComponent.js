// Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
// SPDX-License-Identifier: MIT-0

import React, { useState } from "react";
import axios from "axios";
import { Form, Button, Alert } from "react-bootstrap";

import awsExports from "../aws-exports";

const initialValues = {
    given_name: "",
    family_name: "",
    email: "",
    tenant_name: "",
    tenant_tier: "basic"
};

export const RegisterComponent = () => {
    const [values, setValues] = useState(initialValues);
    const [result, setResult] = useState("");

    function handleInputChange(event) {
        const { name, value } = event.target;
        setValues({
            ...values,
            [name]: value,
        });
    }

    async function handleSubmit(event) {
        event.preventDefault();
        try {
            const response = await axios.post(`${awsExports.api_gateway.regional_endpoint}register`, values);
            console.log(response.data)
            setResult(response.data.message);
        } catch (error) {
            setResult("Something went wrong!");
        }
    }

    return (
<div className="content-container">
            <Form onSubmit={handleSubmit} className="p-5 bg-light rounded shadow" >
                <h2 className="mb-4 text-center">Registration page</h2>

                <Form.Group className="mb-3">
                    <Form.Label>Given Name</Form.Label>
                    <Form.Control type="text" name="given_name" value={values.given_name} onChange={handleInputChange} placeholder="Enter given name" />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Family Name</Form.Label>
                    <Form.Control type="text" name="family_name" value={values.family_name} onChange={handleInputChange} placeholder="Enter family name" />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" name="email" value={values.email} onChange={handleInputChange} placeholder="Enter email" />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Company Name</Form.Label>
                    <Form.Control type="text" name="tenant_name" value={values.tenant_name} onChange={handleInputChange} placeholder="Enter company name" />
                </Form.Group>

                <Form.Group className="mb-3">
                    <Form.Label>Subscription Plan</Form.Label>
                    <Form.Select name="tenant_tier" value={values.tenant_tier} onChange={handleInputChange}>
                        <option value="basic">basic</option>
                        <option value="premium">premium</option>
                    </Form.Select>
                </Form.Group>

                <Button variant="primary" type="submit" className="w-100 mt-3">Register</Button>

                {result && (
                    <Alert variant={result.includes("User registered successfully.") ? "success" : "danger"} className="mt-4 text-center">
                        {result}
                    </Alert>
                )}
            </Form>
        </div>
    );
};
