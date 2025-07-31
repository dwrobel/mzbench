#!/usr/bin/env python

from contextlib import contextmanager
import json
from multiprocessing import Process
import http.server
import socketserver
import random

port = random.randint(8777, 8888)

class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write("welcome")

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))

        if 'color' in body and body['color'] == 'red':
            self.send_response(200)
        else:
            self.send_response(404)

        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write("OHAI")

    def log_message(self, format, *args):
        pass


def serve():
    handler = ServerHandler
    httpd = socketserver.TCPServer(("", port), handler)
    httpd.serve_forever()


@contextmanager
def background_server():
    server = Process(target=serve)
    server.start()
    try:
        yield
    finally:
        server.terminate()

if __name__ == '__main__':
    serve()