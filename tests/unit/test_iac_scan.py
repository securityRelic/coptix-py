'''
Basic Unit Tests

Python REST API Automation
Cloud Optix: Infrastructure as Code (IaC) REST API Endpoint

Author: https://github.com/securityRelic
'''

import unittest
import unittest.mock
import logging
import src.iac_scan

class UnitTestVariables(unittest.TestCase):
    '''
    Coptix-py Unit Tests
    '''
    logging.basicConfig(format='Unit Test [%(levelname)s]: %(message)s', level=logging.DEBUG)

    @unittest.mock.patch('requests.Session.send')
    def test_unit_full_execution(self, mock_post):
        '''
        Test:
            Full Execution
        Type:
            Positive
        Expected Execution:
            - Call to defined API endpoint (mock)
            - successful authN and API interation (mock)
            - Enpoint returns 200 status code and scan
        Assertion:
            Return build_id is equal
        '''
        logging.info('[Unit] IaC scan: Full Execution')
        # Set arguments to test
        mock_post.return_value = unittest.mock.Mock(status_code=200, \
                                                    text=str('{"scan_id":"999999a9-9999-999a-9a9a-99999a99a9a9a9",'
                                                             '"summary":"null"}'))
        file_header = [('files', ('some_filename', 'some_file'))]
        my_key = '7uyhf456-asdf-9087-gh76-k3d98sd4123e' # Not a valid key
        function_return = src.iac_scan.iac_scan(file_header, my_key)
        self.assertEqual("999999a9-9999-999a-9a9a-99999a99a9a9a9", function_return)


    @unittest.mock.patch('requests.Session.send')
    def test_unit_failed_authentication(self, mock_post):
        '''
        Test:
            Failed Authentication
        Type:
            Negative
        Expected Execution:
            - Call to defined API endpoint (mock)
            - Failed Authentication (mock)
            - Enpoint returns 401 status code
        Assertion:
            Return is False
        '''
        logging.info('[Unit] IaC scan: Failed Authentication')
        # Set arguments to test
        mock_post.return_value = unittest.mock.Mock(status_code=401, \
                                      text=str('Unauthorized access or ApiKey expired'))
        file_header = [('files', ('some_filename', 'some_file'))]
        my_key = '7uyhf456-asdf-9087-gh76-k3d98sd4123e' # Not a valid key
        self.assertFalse(src.iac_scan.iac_scan(file_header, my_key))


    def test_unit_key_value_error(self):
        '''
        Test:
            Key ValueError
        Type:
            Negative
        Expected Execution:
            - Identification of bad key format
            - Exception raised
        Assertion:
            ValueError raised
        '''
        logging.info('[Unit] IaC scan: Key ValueError')
        file_header = [('files', ('some_filename', 'some_file'))]
        my_key = '7uyhf456-asdf-9087-gh76-k3d98' # Set key to incorrect format
        # Execute function and validate return
        with self.assertRaises(ValueError):
            src.iac_scan.iac_scan(file_header, my_key)


    def test_unit_key_type_error(self):
        '''
        Test:
            Key TypeError
        Type:
            Negative
        Expected Execution:
        - Identification of bad class type for key
        - Exception raised
        Return Assertion:
            TypeError raised
        '''
        logging.info('[Unit] IaC scan: Key TypeError')
        file_header = [('files', ('some_filename', 'some_file'))]
        my_key = 123456 # Set key to wrong class type
        with self.assertRaises(TypeError):
            src.iac_scan.iac_scan(file_header, my_key)


    def test_unit_file_header_type_error(self):
        '''
        Test:
            File Header TypeError
        Type:
            Negative
        Expected Execution:
            - Validation identifies wrong class type for file header
            - Exception raised
        Return Assertion:
            TypeError raised
        '''
        logging.info('[Unit] IaC scan: File Header TypeError')
        file_header = 12345 #Set file header to wrong class type
        my_key = '7uyhf456-asdf-9087-gh76-k3d98sd4123e' # Not a valid key
        with self.assertRaises(TypeError):
            src.iac_scan.iac_scan(file_header, my_key)
