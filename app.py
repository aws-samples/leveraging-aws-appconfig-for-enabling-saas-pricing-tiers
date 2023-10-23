# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os
from aws_cdk import App

from stacks.identity_stack import IdentityStack
from stacks.config_stack import ConfigStack
from stacks.backend_stack import BackendStack
from stacks.data_stack import DataStack

app = App()

# Get the region from os or default to 'us-east-1'
region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

allowed_regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2"]

if region not in allowed_regions:
    raise ValueError(f"Error: Unsupported region '{region}'. Allowed regions are: {', '.join(allowed_regions)}.")

stack_env = {
    "region": region
}

identity_stack = IdentityStack(app, "IdentityStack", env=stack_env)
config_stack = ConfigStack(app, "ConfigStack", env=stack_env)
data_stack = DataStack(app, "DataStack", env=stack_env)

backend_stack = BackendStack(app, "BackendStack",
    identity_stack=identity_stack,
    config_stack=config_stack,
    data_stack=data_stack,
    env=stack_env
)

# Synthesize the CDK app
app.synth()
