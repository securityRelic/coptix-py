'''
Python REST API Automation
Cloud Optix: Infrastructure as Code (IaC) REST API Endpoint

Author: https://github.com/securityRelic
'''
import logging
import json
import re
import requests

logging.basicConfig(format='coptix-py [%(levelname)s]: %(message)s', level=logging.INFO)

def iac_scan(files: list, key: str) -> (str, bool):
    '''
    Function:
    - With AuthN Key and IaC file(s) test IaC with Cloud Optix scan API

    Preconditions:
    - Caller supplies multipart file as list or tuple (files) and authentication key (key)
    - Basic validation:
        - Authentication key (key) validated as string (TypeError) and key format (ValueError)
        - Multipart file list (files) validated as list or tuple (TypeError)

    Postconditions:
    - With successful (200 status code) API call and return, extract 'scan_id' and return to caller (type str)
    - On none 200 status return False to caller (type bool)
        - 400: ApiKey not provided
        - 400: Unable to retrieve user (When API key cannot be linked to a customer)
        - 400: Proper arguments not provided (When one/more of the mandatory params is not provided properly)
        - 401: Unauthorized access or ApiKey expired
        - 404: No message available (Api resource could not be found)
    '''
    if not isinstance(key, str):
        logging.exception('Key not of correct type')
        raise TypeError

    if not re.match('[a-z0-9]{8}\\-[a-z0-9]{4}\\-[a-z0-9]{4}\\-[a-z0-9]{4}\\-[a-z0-9]{12}', key):
        logging.exception('Authentication key is not in a valid format')
        raise ValueError

    if not isinstance(files, (list, tuple)):
        logging.exception('Files not of correct type')
        raise TypeError

    api_endpoint = 'https://optix.sophos.com/api/v1/iac/scan'
    coptix_key_mod = ''.join(['ApiKey', ' ', key])
    api_authn = {'Authorization': coptix_key_mod}

    try:
        api_session = requests.Session()
        api_request = requests.Request('POST', api_endpoint, headers=api_authn, files=files)
        api_prepped = api_session.prepare_request(api_request)
        api_call = api_session.send(api_prepped)
        api_session.close()
        if api_call.status_code == 200:
            logging.info('API call successful: {} {}'.format(api_call.status_code, api_call.text))
            api_text = json.loads(api_call.text)
            return api_text['scan_id']

        logging.error('API call failed: {} {}'.format(api_call.status_code, api_call.text))
        return False

    except Exception:
        logging.error('Exception: API endpoint call failed')
        raise
