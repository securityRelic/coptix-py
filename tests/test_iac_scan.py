'''
Unit Tests

Python REST API Automation
Cloud Optix: Infrastructure as Code (IaC) REST API Endpoint

Author: https://github.com/securityRelic
'''

import unittest
import unittest.mock
import logging
import os
import iac_scan

class UnitTestVariables(unittest.TestCase):
    '''
    Coptix-py Unit Tests
    '''
    logging.basicConfig(format='UT DOC-BUILD [%(levelname)s]: %(message)s', level=logging.DEBUG)


    def test_iac_scan_good(self):
        '''
        Included for some basic workspace tests.  Drop for CI

        Type: positive
        Test: Good authN and product configuration yaml file
        Result: scan-id
        '''
        logging.info('[UT] IAC SCAN: Good Execution')
        # Set arguments to test
        cf_file = open('../tests/good-cf.yml', 'rb')
        # file_header = ('files', ('good-cf.yml', cf_file))
        file_header = (('files', ('good-cf.yml', cf_file)), ('files', ('good-cf.yml', cf_file)))
        my_key = os.environ.get('COPTIX_KEY')
        # Execute function and validate return
        self.assertTrue(iac_scan.iac_scan(file_header, my_key))
        cf_file.close()


    def test_iac_scan_bad_authn(self):
        '''
        Included for some basic workspace tests.  Drop for CI

        Type: Negative
        Test: Bad authn key
        Result: False
        '''
        logging.info('[UT] IAC SCAN: Bad AuthN')
        # Set arguments to test
        cf_file = open('../tests/good-cf.yml', 'rb')
        file_header = [('files', ('good-cf.yml', cf_file))]
        my_key = '7uyhf456-asdf-9087-gh76-k3d98sd4123e' # Invalid key
        # Execute function and validate return
        self.assertFalse(iac_scan.iac_scan(file_header, my_key))
        cf_file.close()


    @unittest.mock.patch('requests.Session.send')
    def test_iac_scan_good_mock(self, mock_post):
        '''
        Type: positive
        Test: Good authN and product configuration yaml file
        Result: scan-id
        '''
        logging.info('[UT] IAC SCAN: Good Execution w/ Mock')
        # Set arguments to test
        mock_post.return_value = unittest.mock.Mock(status_code=200, \
                                                    text=str('{"scan_id":"999999a9-9999-999a-9a9a-99999a99a9a9a9",'
                                                             '"summary":"null"}'))
        file_header = [('files', ('good-cf.yml', 'This is where the filename would be'))] # Don't need valid entry for mocked api call
        my_key = '7uyhf456-asdf-9087-gh76-k3d98sd4123e' # Don't need a valid key for mock
        # Execute function and validate return
        function_return = iac_scan.iac_scan(file_header, my_key)
        self.assertEqual("999999a9-9999-999a-9a9a-99999a99a9a9a9", function_return)


    @unittest.mock.patch('requests.Session.send')
    def test_iac_scan_bad_authn_mock(self, mock_post):
        '''
        Type: positive
        Test: Good authN and product configuration yaml file
        Result: scan-id
        '''
        logging.info('[UT] IAC SCAN: Bad AuthN w/ Mock')
        # Set arguments to test
        mock_post.return_value = unittest.mock.Mock(status_code=401, \
                                      text=str('Unauthorized access or ApiKey expired'))
        file_header = [('files', ('good-cf.yml', 'This is where the filename would be'))] # Don't need valid entry for mocked api call
        my_key = '7uyhf456-asdf-9087-gh76-k3d98sd4123e' # Don't need a valid key for mock
        # Execute function and validate return
        self.assertFalse(iac_scan.iac_scan(file_header, my_key))


    def test_iac_scan_bad_key_value_error(self):
        '''
        Type: negative
        Test: Bad key
        Result: Exception
        '''
        logging.info('[UT] IAC SCAN: Bad key w/ ValueError')
        file_header = [('files', ('some_filename', 'some_filename'))] # Don't need valid entry for mocked api call
        my_key = '7uyhf456-asdf-9087-gh76-k3d98' # Key too short Don't need a valid key for mock
        # Execute function and validate return
        with self.assertRaises(ValueError):
            iac_scan.iac_scan(file_header, my_key)


    def test_iac_scan_bad_key_type_error(self):
        '''
        Type: negative
        Test: Bad key
        Result: Exception
        '''
        logging.info('[UT] IAC SCAN: Bad key w/ TypeError')
        file_header = [('files', ('some_filename', 'some_filename'))] 
        my_key = 123456 # Key too short Don't need a valid key for mock
        # Execute function and validate return
        with self.assertRaises(TypeError):
            iac_scan.iac_scan(file_header, my_key)


    def test_iac_scan_bad_file_type_error(self):
        '''
        Type: negative
        Test: File (list)
        Result: Exception
        '''
        logging.info('[UT] IAC SCAN: Bad file w/ TypeError')
        file_header = 12345
        my_key = '7uyhf456-asdf-9087-gh76-k3d98sd4123e' 
        # Execute function and validate return
        with self.assertRaises(TypeError):
            iac_scan.iac_scan(file_header, my_key)
