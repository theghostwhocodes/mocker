from http.server import BaseHTTPRequestHandler
import os

import mocker.utils


def MainRequestHandlerFactory(data_path):
    class MainRequestHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.data_path = data_path
            super(BaseHTTPRequestHandler, self).__init__(*args, **kwargs)

        def default_response(self):
            file_path = mocker.utils.compute_file_path(
                self.data_path,
                self.path,
                self.command
            )

            mock_exists = os.path.exists(file_path)
            if mock_exists:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                mock_content = mocker.utils.load_mock(file_path)
                self.wfile.write(mock_content)
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(
                    b'{"message": "The mock for this URL doesn\'t exists"}'
                )

        def do_HEAD(self):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

        def do_GET(self):
            self.default_response()

        def do_POST(self):
            self.default_response()

        def do_PUT(self):
            self.default_response()

        def do_PATCH(self):
            self.default_response()

        def do_DELETE(self):
            self.default_response()

    return MainRequestHandler
