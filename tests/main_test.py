from http.client import HTTPConnection
from http.server import HTTPServer
import unittest

from mocker.http_handlers import MainRequestHandlerFactory


class TestMainRequestHandler(unittest.TestCase):
    def setUp(self):
        self.DATA_PATH = './tests/data'
        self.HOST = '127.0.0.1'
        self.PORT = 8000
        self.SERVER_ADDRESS = (self.HOST, self.PORT)
        MainRequestHandler = MainRequestHandlerFactory(self.DATA_PATH)
        self.httpd = HTTPServer(self.SERVER_ADDRESS, MainRequestHandler)

    def test_basic_url_working(self):
        connection = HTTPConnection(*self.SERVER_ADDRESS)
        connection.request('GET', '/test')
        self.httpd.handle_request()
        response = connection.getresponse()
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')
        connection.close()
        self.httpd.server_close()

    def test_basic_url_not_working(self):
        connection = HTTPConnection(*self.SERVER_ADDRESS)
        connection.request('POST', '/prova')
        self.httpd.handle_request()
        response = connection.getresponse()
        self.assertEqual(response.status, 404)
        self.assertEqual(response.reason, 'Not Found')
        connection.close()
        self.httpd.server_close()
