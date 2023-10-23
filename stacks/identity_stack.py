# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    aws_cognito as cognito
)
from constructs import Construct

class IdentityStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a new Amazon Cognito Userpool
        self.user_pool = cognito.UserPool(
            self, 
            "UserPool",
            sign_in_aliases=cognito.SignInAliases(email=True),
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            custom_attributes={
                'tenant_id': cognito.StringAttribute(mutable=False)
            },
            standard_attributes=cognito.StandardAttributes(
                given_name=cognito.StandardAttribute(
                    required=True,
                    mutable=True
                ),
                family_name=cognito.StandardAttribute(
                    required=True,
                    mutable=True
                ),
                email=cognito.StandardAttribute(
                    required=True,
                    mutable=True
                )
            )
        )
        self.user_pool.apply_removal_policy(RemovalPolicy.DESTROY)

        # Create an App Client for the User Pool
        self.user_pool_client = self.user_pool.add_client("UserPoolClient",
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(implicit_code_grant=True),
                scopes=[cognito.OAuthScope.OPENID, cognito.OAuthScope.PROFILE],
                callback_urls=["http://localhost:3000", "http://localhost:8080"]
            )
        )

        # Output the UserPoolId and ClientId to CloudFormation outputs for easier reference
        CfnOutput(self, "UserPoolId", value=self.user_pool.user_pool_id, description="User Pool ID")
        CfnOutput(self, "UserPoolClientId", value=self.user_pool_client.user_pool_client_id, description="User Pool Client ID")
    
    @property
    def user_pool_obj(self) -> cognito.UserPool:
        return self.user_pool

    @property
    def user_pool_id(self) -> str:
        return self.user_pool.user_pool_id

    @property
    def user_pool_client_id(self) -> str:
        return self.user_pool_client.user_pool_client_id