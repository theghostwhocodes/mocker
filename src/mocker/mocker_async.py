import argparse
import logging
import os

import pkg_resources
from aiohttp import web

import mocker.utils

TCP_PORT = 8080
HOST = '127.0.0.1'


def handle_factory(data_path):

    async def handle(request: web.Request):
        file_path = mocker.utils.compute_file_path(
            data_path,
            request.path,
            request.method
        )
        return web.Response(text=file_path)

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