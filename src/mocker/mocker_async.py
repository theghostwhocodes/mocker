import argparse
import email
import json
import logging
import os
import time

import pkg_resources
from aiohttp import web

import mocker.utils
from mocker.exceptions import JSONKeyMissingException

TCP_PORT = 8080
HOST = '127.0.0.1'

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


def main():
    parser = argparse.ArgumentParser(description='HTTP data mocker')
    parser.add_argument('data_path', help='The data folder')
    parser.add_argument(
        '-p',
        '--port',
        help='The TCP port',
        default=TCP_PORT,
        type=int
    )
    parser.add_argument('--host', help='The host', default=HOST)
    parser.add_argument(
        '-l',
        '--log-file',
        help='save log messages in a given file'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        default=False,
        help='print more detailed log messages'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'Mocker version {pkg_resources.require("mocker")[0].version}'
    )
    args = parser.parse_args()

    logging_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(filename=args.log_file, level=logging_level)

    if os.path.exists(args.data_path):
        app = web.Application()
        app.add_routes([
            web.get('/{tail:.*}', handle_factory(args.data_path))
        ])
        try:
            web.run_app(app, host=args.host, port=args.port)
        except KeyboardInterrupt:
            print('Exiting Mocker...')
    else:
        print('Folder {} not found'.format(args.data_path))


if __name__ == '__main__':
    main()