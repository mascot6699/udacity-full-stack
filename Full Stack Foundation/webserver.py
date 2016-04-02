"""
Practice code for making own webserver
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/umang/"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "<html><body>Hello Umang!</body></html>"
            self.wfile.write(message)
            print message
            return

        if self.path.endswith("/hola/"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body> &#161 Hola ! </body></html>"
            self.wfile.write(message)
            print message
            return
        else:
            self.send_error(404, 'File Not Found: %s. Try hitting /umang/ or /hola/' % self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()