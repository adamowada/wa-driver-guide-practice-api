# api/practice-questions.py
from chatgpt.question_generator import generate_questions

from http.server import BaseHTTPRequestHandler, HTTPServer


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        generated_questions = generate_questions()

        # forming the response
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(generated_questions.encode())


if __name__ == '__main__':
    server_address = ('localhost', 8000)  # use any available port
    httpd = HTTPServer(server_address, handler)  # httpd is a commonly used abbreviation for "HTTP Daemon"
    print(f'Starting httpd server on {server_address[0]}:{server_address[1]}')
    httpd.serve_forever()
