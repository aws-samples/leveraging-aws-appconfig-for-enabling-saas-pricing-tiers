# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json

from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_appconfig as appconfig
)
from constructs import Construct

class ConfigStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # AWS AppConfig setup
        features_config = {
            "analytics": {
                "default": False,
                "rules": {
                    "customer tier equals basic or premium": {
                        "when_match": True,
                        "conditions": [{"action": "KEY_IN_VALUE", "key": "tier", "value": ["basic", "premium"]}],
                    }
                },
            },
            "crm": {
                "default": False,
                "rules": {
                    "customer tier equals basic or premium": {
                        "when_match": True,
                        "conditions": [{"action": "KEY_IN_VALUE", "key": "tier", "value": ["basic", "premium"]}],
                    }
                },
            },
            "email": {
                "default": False,
                "rules": {
                    "customer tier equals premium": {
                        "when_match": True,
                        "conditions": [{"action": "EQUALS", "key": "tier", "value": "premium"}],
                    }
                },
            }
        }

        self.config_app = appconfig.CfnApplication(
            self,
            id="app",
            name="product-features",
        )
        self.config_app.apply_removal_policy(RemovalPolicy.DESTROY)

        self.config_env = appconfig.CfnEnvironment(
            self,
            id="env",
            application_id=self.config_app.ref,
            name="dev-env",
        )
        self.config_env.apply_removal_policy(RemovalPolicy.DESTROY)

        self.config_profile = appconfig.CfnConfigurationProfile(
            self,
            id="profile",
            application_id=self.config_app.ref,
            location_uri="hosted",
            name="features",
        )
        self.config_profile.apply_removal_policy(RemovalPolicy.DESTROY)

        self.hosted_cfg_version = appconfig.CfnHostedConfigurationVersion(
            self,
            "version",
            application_id=self.config_app.ref,
            configuration_profile_id=self.config_profile.ref,
            content=json.dumps(features_config),
            content_type="application/json",
        )
        self.hosted_cfg_version.apply_removal_policy(RemovalPolicy.DESTROY)

        self.app_config_deployment = appconfig.CfnDeployment(
            self,
            id="deploy",
            application_id=self.config_app.ref,
            configuration_profile_id=self.config_profile.ref,
            configuration_version=self.hosted_cfg_version.ref,
            deployment_strategy_id="AppConfig.AllAtOnce",
            environment_id=self.config_env.ref,
        )
        self.app_config_deployment.apply_removal_policy(RemovalPolicy.DESTROY)

    @property
    def config_app_name(self) -> str:
        return self.config_app.name

    @property
    def config_env_name(self) -> str:
        return self.config_env.name

    @property
    def config_profile_name(self) -> str:
        return self.config_profile.name
