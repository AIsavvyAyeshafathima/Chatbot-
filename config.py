#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

""" Bot Configuration """

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    APP_TYPE = os.environ.get("MicrosoftAppType", "MultiTenant")
    APP_TENANTID = os.environ.get("MicrosoftAppTenantId", "")
    # Added to support interaction with Azure AI API key
    ENDPOINT_URI = os.environ.get("MicrosoftAIServiceEndpoint", "https://default.endpoint/")
    API_KEY = os.environ.get("MicrosoftAIServiceAPIKey", "default-key-if-not-set")
    
    # Debugging output to verify values
    print(f"ENDPOINT_URI: {ENDPOINT_URI}")
    print(f"API_KEY: {API_KEY}")
 
    
    


