# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import os
import uuid
import boto3
import logging

# Constants
REGION = os.environ['AWS_REGION']
USER_POOL_ID = os.environ['USER_POOL_ID']
TENANT_METADATA_TABLE_NAME = os.environ['TENANT_METADATA_TABLE_NAME']
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Allow-Headers': 'Content-Type'
}

# AWS service clients
cognito = boto3.client('cognito-idp', region_name=REGION)
dynamodb = boto3.resource('dynamodb', region_name=REGION)

tenant_metadata_table = dynamodb.Table(TENANT_METADATA_TABLE_NAME)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    logger.info('Received Event: %s', event)

    body = json.loads(event['body'])
    tenant_id = str(uuid.uuid4())
    response={}

    try:
        _create_cognito_user(body, tenant_id)
        logger.info(f"Succesfully created user {tenant_id}.")

        _create_tenant_metadata(body, tenant_id)
        logger.info("Succesfully written details to DynamoDB.")

        response = {
            'statusCode': 200,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': f"User registered successfully. Please check your email at {body['email']} for the password."})
        }
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        
        response = {
            'statusCode': 500,
            'headers': CORS_HEADERS,
            'body': json.dumps({'message': f"An error occurred: {e}"})
        }

    return response

def _create_cognito_user(event: dict, tenant_id: str):
    cognito.admin_create_user(
        UserPoolId=USER_POOL_ID,
        Username=event['email'],
        UserAttributes=[
            {'Name': 'given_name', 'Value': event['given_name']},
            {'Name': 'family_name', 'Value': event['family_name']},
            {'Name': 'email', 'Value': event['email']},
            {'Name': 'custom:tenant_id', 'Value': tenant_id}
        ]
    )

def _create_tenant_metadata(event: dict, tenant_id: str):
    tenant_metadata_table.put_item(
        Item={
            'tenant_id': tenant_id,
            'tenant_name': event['tenant_name'],
            'tenant_tier': event['tenant_tier'],
            'fullname': f"{event['given_name']} {event['family_name']}"
        },
        ConditionExpression='attribute_not_exists(tenant_id)'
    )
