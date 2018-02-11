# coding: utf-8
"""Mocker handlers module"""

import json
import os
from http.server import BaseHTTPRequestHandler
import pkg_resources
import mocker.utils
from mocker.exceptions import JSONKeyMissingException


__version__ = pkg_resources.require("mocker")[0].version


def MainRequestHandlerFactory(data_path):
    """Main request handler factory is an utility method that takes some
    variables, inject them to a BaseHTTPRequestHandler and return that handler"""


    class MainRequestHandler(BaseHTTPRequestHandler):
        """This is the main http request handler"""
        
        server_version = "Mocker/" + __version__

        def __init__(self, *args, **kwargs):
            self.data_path = data_path
            super().__init__(*args, **kwargs)
        
        def send_response(self, code, message=None):
            """Add the response header to the headers buffer and log the
            response code.

            Also send two standard headers with the server software
            version and the current date.

            """
            self.log_request(code)
            self.send_response_only(code, message)
            # self.send_header('Server', self.version_string())
            # self.send_header('Date', self.date_time_string())

        def default_response(self):
            """Handles the default response"""
            file_path = mocker.utils.compute_file_path(
                self.data_path,
                self.path,
                self.command
            )

            mock_exists = os.path.exists(file_path)
            if mock_exists:
                try:
                    content_loaded = mocker.utils.load_mock(file_path)
                    response_loaded = content_loaded.get('response', None)
                    if response_loaded is None:
                        raise JSONKeyMissingException(
                            message='You must specify a "response" key in your mock'
                        )
                    
                    content = response_loaded['body']
                    http_status = response_loaded.get('status', 200)
                    headers = response_loaded.get('headers', {})

                    self.send_response(http_status)

                    for key, value in headers.items():
                        self.send_header(key, value)
                    
                    if 'content-type' not in [key.lower() for key in headers]:
                        self.send_header('Content-Type', 'application/json')
                    if 'server' not in [key.lower() for key in headers]:
                        self.send_header('Server', self.version_string())
                    if 'date' not in [key.lower() for key in headers]:
                        self.send_header('Date', self.date_time_string())

                    self.end_headers()
                except json.JSONDecodeError:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Server', self.version_string())
                    self.send_header('Date', self.date_time_string())
                    self.end_headers()
                    content = {
                        "message": "Mock file is not a valid JSON"
                    }
                except JSONKeyMissingException as exc:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Server', self.version_string())
                    self.send_header('Date', self.date_time_string())
                    self.end_headers()
                    content = {
                        "message": exc.message
                    }
                
                self.wfile.write(json.dumps(content).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Server', self.version_string())
                self.send_header('Date', self.date_time_string())
                self.end_headers()
                content = {
                    "message": "The mock for this URL doesn\'t exists"
                }
                self.wfile.write(json.dumps(content).encode('utf-8'))

        def do_HEAD(self):
            """Handles HTTP HEAD verb"""
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header('Server', self.version_string())
            self.send_header('Date', self.date_time_string())
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
