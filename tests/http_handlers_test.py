import json
import unittest
from http.client import HTTPConnection
from http.server import HTTPServer

from mocker.http_handlers import handle_factory
from aiohttp.test_utils import TestClient,TestServer, loop_context
from aiohttp import web


class TestHttpHandlers(unittest.TestCase):

    def setUp(self):
        self.DATA_PATH = './tests/data'
        self.HOST = '127.0.0.1'
        self.PORT = 8000
        self.SERVER_ADDRESS = (self.HOST, self.PORT)
        self.app = web.Application()
        self.app.add_routes([
            web.get('/{tail:.*}', handle_factory(self.DATA_PATH)),
            web.post('/{tail:.*}', handle_factory(self.DATA_PATH)),
            web.put('/{tail:.*}', handle_factory(self.DATA_PATH)),
            web.patch('/{tail:.*}', handle_factory(self.DATA_PATH)),
            web.head('/{tail:.*}', handle_factory(self.DATA_PATH)),
            web.delete('/{tail:.*}', handle_factory(self.DATA_PATH)),
            web.options('/{tail:.*}', handle_factory(self.DATA_PATH)),
        ])
        self.test_server = TestServer(self.app, host=self.HOST, port=self.PORT)
        # web.run_app(self.app, host=self.HOST, port=self.PORT)

    def test_mock_exists(self):
        with loop_context() as loop:
            async def test():
                async with TestClient(self.test_server, loop=loop) as client:
                    # nonlocal client
                    response = await client.get('/test')

                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.reason, 'OK')

                    headers = response.headers
                    self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')
                    self.assertIn('Mocker/', headers['Server'])

            loop.run_until_complete(test())

    def test_mock_exists_head(self):
        with loop_context() as loop:
            async def test():
                async with TestClient(self.test_server, loop=loop) as client:
                    # nonlocal client
                    response = await client.head('/test')

                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.reason, 'OK')

                    headers = response.headers
                    self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')
                    self.assertIn('Mocker/', headers['Server'])
                    self.assertIn('Date', headers)

            loop.run_until_complete(test())

    def test_mock_exists_post(self):
        with loop_context() as loop:
            async def test():
                async with TestClient(self.test_server, loop=loop) as client:
                    # nonlocal client
                    response = await client.post('/test')

                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.reason, 'OK')

                    headers = response.headers
                    self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')
                    self.assertIn('Mocker/', headers['Server'])
                    self.assertIn('Date', headers)

            loop.run_until_complete(test())

    def test_mock_exists_put(self):
        with loop_context() as loop:
            async def test():
                async with TestClient(self.test_server, loop=loop) as client:
                    # nonlocal client
                    response = await client.put('/test')

                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.reason, 'OK')

                    headers = response.headers
                    self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')
                    self.assertIn('Mocker/', headers['Server'])
                    self.assertIn('Date', headers)

            loop.run_until_complete(test())

    def test_mock_exists_patch(self):
        with loop_context() as loop:
            async def test():
                async with TestClient(self.test_server, loop=loop) as client:
                    # nonlocal client
                    response = await client.patch('/test')

                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.reason, 'OK')

                    headers = response.headers
                    self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')
                    self.assertIn('Mocker/', headers['Server'])
                    self.assertIn('Date', headers)

            loop.run_until_complete(test())

    def test_mock_exists_delete(self):
        with loop_context() as loop:
            async def test():
                async with TestClient(self.test_server, loop=loop) as client:
                    # nonlocal client
                    response = await client.delete('/test')

                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.reason, 'OK')

                    headers = response.headers
                    self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')
                    self.assertIn('Mocker/', headers['Server'])
                    self.assertIn('Date', headers)

            loop.run_until_complete(test())

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
    def test_mock_exists_no_date_header(self):
        connection = HTTPConnection(*self.SERVER_ADDRESS)
        connection.request('GET', '/test-no-server-header')
        self.httpd.handle_request()
        response = connection.getresponse()

        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')

        headers = response.getheaders()
        self.assertEqual(headers[2][0], 'Date')

        connection.close()
        self.httpd.server_close()

    @unittest.skip
    def test_mock_exists_custom_content_type(self):
        connection = HTTPConnection(*self.SERVER_ADDRESS)
        connection.request('GET', '/test-custom-content-type')
        self.httpd.handle_request()
        response = connection.getresponse()

        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')

        headers = response.getheaders()
        self.assertEqual(headers[0][0], 'Content-Type')
        self.assertEqual(headers[0][1], 'application/mocker')
        self.assertEqual(headers[1][0], 'Server')
        self.assertIn('Mocker/', headers[1][1])

        connection.close()
        self.httpd.server_close()

    @unittest.skip
    def test_mock_exists_custom_server_header(self):
        connection = HTTPConnection(*self.SERVER_ADDRESS)
        connection.request('GET', '/test-custom-server-header')
        self.httpd.handle_request()
        response = connection.getresponse()

        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')

        headers = response.getheaders()
        self.assertEqual(headers[1][0], 'Server')
        self.assertIn('MockerCustom', headers[1][1])

        connection.close()
        self.httpd.server_close()

    @unittest.skip
    def test_mock_exists_custom_date_header(self):
        connection = HTTPConnection(*self.SERVER_ADDRESS)
        connection.request('GET', '/test-custom-date-header')
        self.httpd.handle_request()
        response = connection.getresponse()

        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, 'OK')

        headers = response.getheaders()
        self.assertEqual(headers[1][0], 'Date')
        self.assertIn('20180201', headers[1][1])

        connection.close()
        self.httpd.server_close()
