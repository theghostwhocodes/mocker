import argparse
from http.server import HTTPServer
import os

from handlers import MainRequestHandlerFactory


TCP_PORT = 8080
HOST = '127.0.0.1'


def main():
    parser = argparse.ArgumentParser(description='HTTP data mocker')
    parser.add_argument('data_path', help='The data folder')
    parser.add_argument(
        '-p',
        '--port',
        help='The TCP port',
        default=TCP_PORT,
        type=int)
    parser.add_argument('--host', help='The host', default=HOST)
    args = parser.parse_args()

    if os.path.exists(args.data_path):
        server_address = (args.host, args.port)
        print('Starting mocker HTTP server at {}:{}'.format(*server_address))
        MainRequestHandler = MainRequestHandlerFactory(args.data_path)
        httpd = HTTPServer(server_address, MainRequestHandler)
        httpd.serve_forever()
    else:
        print('Folder {} not found'.format(args.data_path))


main()
