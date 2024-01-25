from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import cgi

class MyHttpRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write("<html><body><h1>Hello, world11!</h1></body></html>".encode('utf-8'))
        return

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.get('content-length'))
            postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write("<html><body><h1>POST data received:</h1>\n".encode('utf-8'))
        self.wfile.write("<pre>{}</pre>\n".format(postvars).encode('utf-8'))
        return

def run(server_class=HTTPServer, handler_class=MyHttpRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
