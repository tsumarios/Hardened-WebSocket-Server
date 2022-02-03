#!/usr/bin/env python3

import json
import logging
import signal
import sys
import ssl
from http.server import HTTPServer, SimpleHTTPRequestHandler
from SimpleWebSocketServer import WebSocket, SimpleWebSocketServer, SimpleSSLWebSocketServer
from threading import Thread
from optparse import OptionParser


logging.basicConfig(level=logging.INFO)


def simulate_auth_server_check(token):
    # Simulate a check request to the auth server
    return token == 'ebfb7ff0-b2f6-41c8-bef3-4fba17be410c'


def login_required(func):
    def wrapper_login_required(self, *args, **kwargs):
        if not self.authenticated:  # Not (yet) authenticated
            token = json.loads(self.data).get('token', '')
            self.authenticated = simulate_auth_server_check(token)  # Check if token is valid
            if not self.authenticated:
                logging.info('> Client unauthenticated %s' % self.address[0])
                self.close(1011, u'unauthenticated')
            else:
                logging.info('> Client authenticated %s' % self.address[0])
                self.sendMessage('Successfully authenticated.')
        else:   # Regular handling if already authenticated
            func(self, *args, **kwargs)
    return wrapper_login_required


class SimpleEchoHandler(WebSocket):
    authenticated = False

    @login_required
    def handleMessage(self):
        data = json.loads(self.data)
        logging.info('> Received msg from %s: %s' % (self.address[0], data))
        self.sendMessage(json.dumps(data))

    def handleConnected(self):
        logging.info('> Client connected %s' % self.address[0])

    def handleClose(self):
        logging.info('> Client disconnected %s' % self.address[0])



def main():
    # Arguments parsing
    parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    parser.add_option("--host", default='', type='string', action="store", dest="host", help="hostname (localhost)")
    parser.add_option("--port", default=5678, type='int', action="store", dest="port", help="port (5678)")
    parser.add_option("--ssl", default=0, type='int', action="store", dest="ssl", help="ssl (1: on, 0: off (default))")
    parser.add_option("--cert", default='./cert.pem', type='string', action="store", dest="cert", help="cert (./cert.pem)")
    parser.add_option("--key", default='./key.pem', type='string', action="store", dest="key", help="key (./key.pem)")
    parser.add_option("--ver", default=ssl.PROTOCOL_TLSv1, type=int, action="store", dest="ver", help="ssl version")

    (options, args) = parser.parse_args()

    if options.ssl == 1:    # $ openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem
        ws_server = SimpleSSLWebSocketServer(options.host, options.port, SimpleEchoHandler, options.cert, options.key, version=options.ver)
        httpd = HTTPServer(('', 443), SimpleHTTPRequestHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True, certfile='./cert.pem', keyfile='./key.pem', ssl_version=ssl.PROTOCOL_TLSv1)
    else:
        ws_server = SimpleWebSocketServer(options.host, options.port, SimpleEchoHandler)
        httpd = HTTPServer(('', 80), SimpleHTTPRequestHandler)

    # Graceful shutdown handling
    def close_sig_handler(signal, frame):
        ws_server.close()
        if options.ssl == 1:
            httpd.shutdown()
            http_server_t.join()
        sys.exit()

    signal.signal(signal.SIGINT, close_sig_handler)

    # Start the HTTP(S) server in a thread
    http_server_t = Thread(target=httpd.serve_forever, daemon=True)
    http_server_t.start()
    # Start the WebSocket server
    ws_server.serveforever()


if __name__ == "__main__":
    main()
