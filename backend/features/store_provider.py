# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import requests
from typing import Any, Dict

from botocore.exceptions import ClientError

from aws_lambda_powertools.utilities.feature_flags.base import StoreProvider
from aws_lambda_powertools.utilities.feature_flags.exceptions import ConfigurationStoreError

class AppConfigStoreProvider(StoreProvider):
    def __init__(self, config_app: str, config_env: str, config_profile: str):
        # Initialize the client to your custom store provider

        super().__init__()

        self.config_app = config_app
        self.config_env = config_env
        self.config_profile = config_profile

    def _get_config(self) -> Dict[str, Any]:
        # Retrieve the config
        url = f'http://localhost:2772/applications/{self.config_app}/environments/{self.config_env}/configurations/{self.config_profile}'

        try:
            response = requests.get(url, timeout=3)
            config = response.text
            return json.loads(config)
        except ClientError as exc:
            raise ConfigurationStoreError("Unable to get AppConfig Store Provider configuration file") from exc

    def get_configuration(self) -> Dict[str, Any]:
        return self._get_config()

    @property
    def get_raw_configuration(self) -> Dict[str, Any]:
        return self._get_config()
