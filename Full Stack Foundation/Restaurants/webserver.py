"""
Practice code for making own webserver
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import views


class WebServerHandler(BaseHTTPRequestHandler):

    form = '''<form method='POST' enctype='multipart/form-data' action='/umang/'>
              <h2>What would you like me to say?</h2>
              <input name="message" type="text" >
              <input type="submit" value="Submit">
              </form>
           '''

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
            message = "<html><body> To create a new restaurant fill this form and click save <br><br><br>"
            message += WebServerHandler.form
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return

        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = "<html><body> To create a new restaurant fill this form and click save <br><br><br>"
            message += WebServerHandler.form
            message += "</body></html>"
            self.wfile.write(message)
            print message
            return
        else:
            self.send_error(404, 'File Not Found: %s. Try hitting /restaurants' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':  # checks is form data is recieved
                fields = cgi.parse_multipart(self.rfile, pdict)  # collects all fields in a form
                messagecontent = fields.get('message')  # store value of message field and store in an array
                message = "<html><body>"
                message += " <h2> Okay, how about this: </h2>"
                message += "<h1> %s </h1>" % messagecontent[0]
                message += WebServerHandler.form
                message += "</body></html>"
                self.wfile.write(message)
                print message
            else:
                self.send_error(404, 'File Not Found: %s. Try hitting /umang/ or /hola/ or '
                                     'hit with multipart/form-data ' % self.path)
        except:
            pass


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