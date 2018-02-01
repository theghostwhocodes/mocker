import json
import unittest
from http.client import HTTPConnection
from http.server import HTTPServer

from mocker.http_handlers import MainRequestHandlerFactory


class TestHttpHandlers(unittest.TestCase):
    
    def setUp(self):
        self.DATA_PATH = './tests/data'
        self.HOST = '127.0.0.1'
        self.PORT = 8000
        self.SERVER_ADDRESS = (self.HOST, self.PORT)
        MainRequestHandler = MainRequestHandlerFactory(self.DATA_PATH)
        self.httpd = HTTPServer(self.SERVER_ADDRESS, MainRequestHandler)
    
    def test_mock_exists(self):
        connection = HTTPConnection(*self.SERVER_ADDRESS)
        connection.request('GET', '/test')
        self.httpd.handle_request()
        response = connection.getresponse()

        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')

        headers = response.getheaders()
        self.assertEqual(headers[0][0], 'Content-Type')
        self.assertEqual(headers[0][1], 'application/json')
        self.assertEqual(headers[1][0], 'Server')
        self.assertIn('Mocker/', headers[1][1])

        connection.close()
        self.httpd.server_close()
    
    def test_mock_does_not_exists(self):
        connection = HTTPConnection(*self.SERVER_ADDRESS)
        connection.request('GET', '/test-not-exists')
        self.httpd.handle_request()
        response = connection.getresponse()
        
        self.assertEqual(response.status, 404)
        self.assertEqual(response.reason, 'Not Found')
        
        headers = response.getheaders()
        self.assertEqual(headers[0][0], 'Content-Type')
        self.assertEqual(headers[0][1], 'application/json')
        self.assertEqual(headers[1][0], 'Server')
        self.assertIn('Mocker/', headers[1][1])
        connection.close()
        self.httpd.server_close()
    
    def test_mock_exists_with_no_response_key(self):
        connection = HTTPConnection(*self.SERVER_ADDRESS)
        connection.request('GET', '/test-no-response')
        self.httpd.handle_request()
        response = connection.getresponse()
        
        self.assertEqual(response.status, 500)
        self.assertEqual(response.reason, 'Internal Server Error')

        headers = response.getheaders()
        self.assertEqual(headers[0][0], 'Content-Type')
        self.assertEqual(headers[0][1], 'application/json')
        self.assertEqual(headers[1][0], 'Server')
        self.assertIn('Mocker/', headers[1][1])

        response_json = json.loads(response.read().decode('utf-8'))
        self.assertDictEqual(
            response_json,
            {
                'message': 'You must specify a "response" key in your mock'
            }
        )
        connection.close()
        self.httpd.server_close()
    
    def test_mock_exists_but_invalid_json(self):
        connection = HTTPConnection(*self.SERVER_ADDRESS)
        connection.request('GET', '/test-invalid-json')
        self.httpd.handle_request()
        response = connection.getresponse()
        
        self.assertEqual(response.status, 500)
        self.assertEqual(response.reason, 'Internal Server Error')

        headers = response.getheaders()
        self.assertEqual(headers[0][0], 'Content-Type')
        self.assertEqual(headers[0][1], 'application/json')
        self.assertEqual(headers[1][0], 'Server')
        self.assertIn('Mocker/', headers[1][1])

        response_json = json.loads(response.read().decode('utf-8'))
        self.assertDictEqual(
            response_json,
            {
                'message': 'Mock file is not a valid JSON'
            }
        )
        connection.close()
        self.httpd.server_close()
    
    def test_mock_exists_no_content_type(self):
        connection = HTTPConnection(*self.SERVER_ADDRESS)
        connection.request('GET', '/test-no-content-type')
        self.httpd.handle_request()
        response = connection.getresponse()

        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')

        headers = response.getheaders()
        self.assertEqual(headers[0][0], 'Content-Type')
        self.assertEqual(headers[0][1], 'application/json')
        self.assertEqual(headers[1][0], 'Server')
        self.assertIn('Mocker/', headers[1][1])

        connection.close()
        self.httpd.server_close()
    
    def test_mock_exists_no_server_header(self):
        connection = HTTPConnection(*self.SERVER_ADDRESS)
        connection.request('GET', '/test-no-server-header')
        self.httpd.handle_request()
        response = connection.getresponse()

        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')

        headers = response.getheaders()
        self.assertEqual(headers[1][0], 'Server')
        self.assertIn('Mocker/', headers[1][1])
        
        connection.close()
        self.httpd.server_close()
