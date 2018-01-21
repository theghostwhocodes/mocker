# coding: utf-8
"""Mocker handlers module"""

from http.server import BaseHTTPRequestHandler
import os

import mocker.utils


def MainRequestHandlerFactory(data_path):
    """Main request handler factory is an utility method that takes some
    variables, inject them to a BaseHTTPRequestHandler and return that handler"""
    class MainRequestHandler(BaseHTTPRequestHandler):
        """This is the main http request handler"""

        def __init__(self, *args, **kwargs):
            self.data_path = data_path
            super().__init__(*args, **kwargs)

        def default_response(self):
            """Handles the default response"""
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
            """Handles HTTP HEAD verb"""
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

        def do_GET(self):
            """Handles HTTP GET verb"""
            self.default_response()

        def do_POST(self):
            """Handles HTTP POST verb"""
            self.default_response()

        def do_PUT(self):
            """Handles HTTP PUT verb"""
            self.default_response()

        def do_PATCH(self):
            """Handles HTTP PATCH verb"""
            self.default_response()

        def do_DELETE(self):
            """Handles HTTP DELETE verb"""
            self.default_response()

    return MainRequestHandler
