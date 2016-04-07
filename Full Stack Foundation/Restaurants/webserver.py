"""
Practice code for making own webserver
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import views, utils


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = views.get_restaurant_list_template()
            self.wfile.write(message)
            return

        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = views.get_create_new_restaurant_form()
            self.wfile.write(message)
            return

        if self.path.endswith("/edit"):
            id = self.path.split("/")[2]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = views.get_edit_restaurant_form(id)
            self.wfile.write(message)
        else:
            self.send_error(404, 'File Not Found: %s. Try hitting /restaurants' % self.path)

    def do_POST(self):
        if self.path.endswith("/restaurants/new"):
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('name')
                utils.create_restaurant(name=messagecontent[0])
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

        if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('name')
                    id = self.path.split("/")[2]
                    utils.rename_restaurant(id, messagecontent[0])
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web server running...open localhost:%s/restaurants in your browser" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()