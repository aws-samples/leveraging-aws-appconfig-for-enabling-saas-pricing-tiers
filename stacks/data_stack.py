# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_dynamodb as dynamodb,
)
from constructs import Construct

class DataStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Amazon DynamoDB Table for Tenant Metadata
        self.tenant_metadata_table = dynamodb.Table(self, "TenantMetadataTable",
            partition_key=dynamodb.Attribute(
                name="tenant_id",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

    @property
    def table_obj(self) -> dynamodb.Table:
        return self.tenant_metadata_table
    
    @property
    def table_name(self) -> str:
        return self.tenant_metadata_table.table_name

    @property
    def table_arn(self) -> str:
        return self.tenant_metadata_table.table_arn
