import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from Parsers import XMLParser, populationInstanceParser




class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        problem, instance = populationInstanceParser(post_data)

        parser = XMLParser('C:\\Users\\Gasper\\Desktop\\satelliteScheduling\\' + problem)
        problem = parser.getProblem()
        response = problem.evaluateSolution(instance)

        self._set_headers()
        self.wfile.write(json.dumps(response).encode())


def run(server_class=HTTPServer, handler_class=Server, port=8008):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port:', port)

    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

