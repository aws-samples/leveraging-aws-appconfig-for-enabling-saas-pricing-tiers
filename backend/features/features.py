# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import os
import json

from aws_lambda_powertools.utilities.feature_flags.feature_flags import FeatureFlags
from aws_lambda_powertools import Logger

from store_provider import AppConfigStoreProvider

logger = Logger()

# Constants
REGION = os.environ['AWS_REGION']
CONFIG_APP_NAME = os.environ['CONFIG_APP_NAME']
CONFIG_ENV_NAME = os.environ['CONFIG_ENV_NAME']
CONFIG_PROFILE_NAME = os.environ['CONFIG_PROFILE_NAME']

appconfig_store = AppConfigStoreProvider(
    config_app=CONFIG_APP_NAME,
    config_env=CONFIG_ENV_NAME,
    config_profile=CONFIG_PROFILE_NAME
)
feature_flags = FeatureFlags(store=appconfig_store)

def lambda_handler(event, context):

    logger.info(f'Received Event: {event}')

    tenant_id = event['requestContext']['authorizer']['tenant_id']

    logger.structure_logs(append=True, tenant_id=tenant_id)
    logger.info(f"Processing request for tenant ID: {tenant_id}")

    fullname = event['requestContext']['authorizer']['fullname']
    tenant = event['requestContext']['authorizer']['tenant_name']
    tier = event['requestContext']['authorizer'].get("tenant_tier", "basic")

    # all_features is evaluated to ["feature1", "feature2"]
    all_features = feature_flags.get_enabled_features(context={"tier": tier})

    logger.info(f"Enabled features for tenant ID {tenant_id}: {all_features}")
    
    return {
        "statusCode": 200,
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Authorization'
        },
        "body": json.dumps({
            "fullname": fullname,
            "tenant": tenant,
            "tier": tier,
            "features": all_features,
        })
    }
