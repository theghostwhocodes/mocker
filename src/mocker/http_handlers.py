import email
import json
import os
import time

import pkg_resources
from aiohttp import web

import mocker.utils
from mocker.exceptions import JSONKeyMissingException


__version__ = pkg_resources.require("mocker")[0].version


def date_time_string(timestamp=None):
    """Return the current date and time formatted for a message header."""
    if timestamp is None:
        timestamp = time.time()
    return email.utils.formatdate(timestamp, usegmt=True)


def handle_factory(data_path):

    async def handle(request: web.Request):
        file_path = mocker.utils.compute_file_path(
            data_path,
            request.path,
            request.method
        )

        response = web.Response()

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

                response.set_status(http_status)

                for key, value in headers.items():
                    response.headers[key] = value

                if 'content-type' not in [key.lower() for key in headers]:
                    response.headers['Content-Type'] = 'application/json'
                if 'server' not in [key.lower() for key in headers]:
                    response.headers['Server'] = "Mocker/" + __version__
                if 'date' not in [key.lower() for key in headers]:
                    response.headers['Date'] = date_time_string()

            except json.JSONDecodeError:
                response.set_status(500)
                response.headers['Content-Type'] = 'application/json'
                response.headers['Server'] = "Mocker/" + __version__
                response.headers['Date'] = date_time_string()
                content = {
                    "message": "Mock file is not a valid JSON"
                }
            except JSONKeyMissingException as exc:
                response.set_status(500)
                response.headers['Content-Type'] = 'application/json'
                response.headers['Server'] = "Mocker/" + __version__
                response.headers['Date'] = date_time_string()
                content = {
                    "message": exc.message
                }

            response.text = json.dumps(content)
        else:
            response.set_status(404)
            response.headers['Content-Type'] = 'application/json'
            response.headers['Server'] = "Mocker/" + __version__
            response.headers['Date'] = date_time_string()
            content = {
                "message": "The mock for this URL doesn\'t exists"
            }
            response.text = json.dumps(content)

        return response

    return handle
