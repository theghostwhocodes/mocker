import argparse
import os
from http.server import HTTPServer

from handlers import MainRequestHandlerFactory


TCP_PORT = 8080
HOST = '127.0.0.1'


def main():
    parser = argparse.ArgumentParser(description='HTTP data mocker')
    parser.add_argument('data_path', help='The data folder')
    args = parser.parse_args()
    if os.path.exists(args.data_path):
        server_address = (HOST, TCP_PORT)
        print('Starting mocker HTTP server at {}:{}'.format(*server_address))
        MainRequestHandler = MainRequestHandlerFactory(args.data_path)
        httpd = HTTPServer(server_address, MainRequestHandler)
        httpd.serve_forever()
    else:
        print('Folder {} not found'.format(args.data_path))


main()
