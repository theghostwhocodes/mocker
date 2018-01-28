# coding: utf-8
"""Mocker handlers module"""

import json
import mocker.utils
import os
from http.server import BaseHTTPRequestHandler
from mocker.exceptions import JSONKeyMissingException



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
                try:
                    content_loaded = mocker.utils.load_mock(file_path)
                    response_loaded = content_loaded.get('response', None)
                    if response_loaded is None:
                        raise JSONKeyMissingException(
                            message='You must specify a "response" key in your mock'
                        )
                    
                    content = response_loaded['body']

                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                except IOError:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    content = {
                        "message": "Mocker encountered an error while opening the file"
                    }
                except json.JSONDecodeError:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    content = {
                        "message": "Mock file is not a valid JSON"
                    }
                except JSONKeyMissingException as exc:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    content = {
                        "message": exc.message
                    }
                
                self.wfile.write(json.dumps(content).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                content = {
                    "message": "The mock for this URL doesn\'t exists"
                }
                self.wfile.write(json.dumps(content).encode('utf-8'))

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
