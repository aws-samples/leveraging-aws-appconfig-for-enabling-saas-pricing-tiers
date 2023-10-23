# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (
    Stack,
    CfnOutput,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_lambda_python_alpha as pylambda,
    aws_iam as iam,
    aws_apigateway as apigateway
)
from constructs import Construct

from stacks.data_stack import DataStack
from stacks.identity_stack import IdentityStack
from stacks.config_stack import ConfigStack

# Constants for layer ARNs
APPCONFIG_EXT_ARN = {
    'us-east-1': 'arn:aws:lambda:us-east-1:027255383542:layer:AWS-AppConfig-Extension:113',
    'us-east-2': 'arn:aws:lambda:us-east-2:728743619870:layer:AWS-AppConfig-Extension:81',
    'us-west-1': 'arn:aws:lambda:us-west-1:958113053741:layer:AWS-AppConfig-Extension:124',
    'us-west-2': 'arn:aws:lambda:us-west-2:359756378197:layer:AWS-AppConfig-Extension:146',
    # Additional regions. See here: https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-integration-lambda-extensions-versions.html#appconfig-integration-lambda-extensions-enabling-x86-64
}
POWERTOOLS_ARN = 'arn:aws:lambda:{}:017000801446:layer:AWSLambdaPowertoolsPythonV2:20'


class BackendStack(Stack):
    def __init__(self, scope: Construct, id: str, data_stack: DataStack, identity_stack: IdentityStack, config_stack: ConfigStack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # Environment Variables
        self.env_vars = {
            "TENANT_METADATA_TABLE_NAME": data_stack.table_name,
            "USER_POOL_ID": identity_stack.user_pool_id,
            "USER_POOL_CLIENT_ID": identity_stack.user_pool_client_id,
            "CONFIG_APP_NAME": config_stack.config_app_name,
            "CONFIG_ENV_NAME": config_stack.config_env_name,
            "CONFIG_PROFILE_NAME": config_stack.config_profile_name
        }

        # AWS Lambda roles
        self.authorizer_role = iam.Role(self, "AuthorizerLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")]    
        )
        self.authorizer_role.apply_removal_policy(RemovalPolicy.DESTROY)
        data_stack.table_obj.grant(self.authorizer_role, "dynamodb:GetItem")

        self.register_role = iam.Role(self, "RegisterLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")]    
        )
        self.register_role.apply_removal_policy(RemovalPolicy.DESTROY)
        data_stack.table_obj.grant(self.register_role, "dynamodb:Query", "dynamodb:PutItem")
        identity_stack.user_pool_obj.grant(self.register_role, "cognito-idp:AdminCreateUser")

        self.features_role = iam.Role(self, "FeaturesLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")],
            inline_policies={"AppConfigPolicy": iam.PolicyDocument(statements=[
                iam.PolicyStatement(
                    actions=["appconfig:GetLatestConfiguration", "appconfig:StartConfigurationSession"],
                    resources=['arn:aws:appconfig:{}:{}:*'.format(self.region, self.account)]
                )
            ])}
        )
        self.features_role.apply_removal_policy(RemovalPolicy.DESTROY)

        # Lambda Layers
        powertools = _lambda.LayerVersion.from_layer_version_arn(self, "PowerTools", POWERTOOLS_ARN.format(self.region))
        try:
            appconfig_extention = _lambda.LayerVersion.from_layer_version_arn(self, "AppConfigExtention", APPCONFIG_EXT_ARN[self.region])
        except KeyError:
            raise ValueError("No ARN defined for region {}".format(self.region))

        # Authorizer Lambda
        self.authorizer_lambda = pylambda.PythonFunction(self, "AuthorizerLambda",
            role=self.authorizer_role,
            runtime=_lambda.Runtime.PYTHON_3_11,
            entry="backend/authorizer",
            index="authorizer.py",
            handler="lambda_handler",
            layers=[powertools],
            environment=self.env_vars
        )
        self.authorizer_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        # Features Lambda
        self.features_lambda = pylambda.PythonFunction(self, "FeaturesLambda",
            role=self.features_role,
            runtime=_lambda.Runtime.PYTHON_3_11,
            entry="backend/features",
            index="features.py",
            handler="lambda_handler",
            layers=[
                powertools,
                appconfig_extention
            ],
            environment=self.env_vars
        )
        self.features_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        # Register Lambda
        self.register_lambda = pylambda.PythonFunction(self, "RegisterLambda",
            role=self.register_role,
            runtime=_lambda.Runtime.PYTHON_3_11,
            entry="backend/register",
            index="register.py",
            handler="lambda_handler",
            layers=[powertools],
            environment=self.env_vars
        )
        self.register_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        # API Gateway Setup
        self.api = apigateway.RestApi(self, "BackendApi",
            endpoint_configuration=apigateway.EndpointConfiguration(
                types=[apigateway.EndpointType.REGIONAL]
            ),
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Origin", "Accept"]
                )
            )
        self.api.apply_removal_policy(RemovalPolicy.DESTROY)

        self.authorizer = apigateway.TokenAuthorizer(self, "ApiAuthorizer", handler=self.authorizer_lambda)
        self.authorizer.apply_removal_policy(RemovalPolicy.DESTROY)

        self.features_resource = self.api.root.add_resource("features")
        self.features_resource.add_method("GET",
            integration=apigateway.LambdaIntegration(handler=self.features_lambda),
            authorizer=self.authorizer
        )
        self.register_resource = self.api.root.add_resource("register")
        self.register_resource.add_method("POST",
            integration=apigateway.LambdaIntegration(handler=self.register_lambda)
        )

        # Output the BackendApi CloudFormation outputs for easier reference
        CfnOutput(self, "BackendApiURL", value=self.api.url, description="Backend Api URL")
    
    @property
    def api_url(self) -> str:
        return self.api.url

