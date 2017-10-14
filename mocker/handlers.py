from http.server import BaseHTTPRequestHandler
import os


def MainRequestHandlerFactory(data_path):
    class MainRequestHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self.data_path = data_path
            super(BaseHTTPRequestHandler, self).__init__(*args, **kwargs)

        def default_response(self, command, path_):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()

            file_path = os.path.join(self.data_path, f'{path_[1:]}.{command}.json')
            with open(file_path, 'rb') as f:
                self.wfile.write(f.read())

        def do_HEAD(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def do_GET(self):
            self.default_response(self.command, self.path)

        def do_POST(self):
            self.default_response(self.command, self.path)

        def do_PUT(self):
            self.default_response(self.command, self.path)

        def do_PATCH(self):
            self.default_response(self.command, self.path)

        def do_DELETE(self):
            self.default_response(self.command, self.path)

    return MainRequestHandler
