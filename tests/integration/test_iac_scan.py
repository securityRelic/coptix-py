'''
Basic Integration Tests

Python REST API Automation
Cloud Optix: Infrastructure as Code (IaC) REST API Endpoint

Author: https://github.com/securityRelic
'''

import unittest
import logging
import os
import src.iac_scan

class UnitTestVariables(unittest.TestCase):
    '''
    Coptix-py integration tests
    '''
    logging.basicConfig(format='Integration Test [%(levelname)s]: %(message)s', level=logging.DEBUG)


    def test_integration_positve_full_execution(self):
        '''
        Test:
            Full Execution
        Type:
            Positive
        Expected Execution:
            - Call to defined API endpoint
            - successful authN and API interation
            - Enpoint returns 200 status code and scan
        Assertion:
            Return is True
        '''
        logging.info('[Integration] IAC SCAN: Full Execution')
        cf_file = open('tests/good-cf.yml', 'rb')
        file_header = [('files', ('good-cf.yml', cf_file))]
        my_key = os.environ.get('COPTIX_KEY')
        self.assertTrue(src.iac_scan.iac_scan(file_header, my_key))
        cf_file.close()


    def test_integration_negative_authn_failure(self):
        '''
        Test:
            Authentication Failure
        Type:
            Negative
        Expected Execution:
            - Call to defined API endpoint
            - Failed Authentication
            - Enpoint returns 401 status code
        Assertion:
            Return is False
        '''
        logging.info('[Integration] IAC SCAN: Authentication Failure')
        cf_file = open('tests/good-cf.yml', 'rb')
        file_header = [('files', ('good-cf.yml', cf_file))]
        my_key = '7uyhf456-asdf-9087-gh76-k3d98sd4123e' # Invalid key
        self.assertFalse(src.iac_scan.iac_scan(file_header, my_key))
        cf_file.close()
