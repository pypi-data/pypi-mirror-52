# coding: utf-8

import mimetypes
import os
import socket
import sys
import webbrowser

from socketserver import ThreadingMixIn
from socketserver import TCPServer
from http.server import SimpleHTTPRequestHandler

from ..utils import fatal_error


class Serve(object):
    @staticmethod
    def serve(document_root=None, host="localhost", port="8000", *args, **kwargs):
        if document_root is not None:
            os.chdir(document_root)
        try:
            httpd = SimpleServe((host, port), SimpleRequests)
        except socket.error:
            return fatal_error("Could not open the webserver at the requested (%s) port" % port)
        webbrowser.open("http://%s:%s" % (host, port))
        try:
            httpd.serve_forever()
        except (KeyboardInterrupt, SystemExit):
            print("Done serving. Goodbye.")
            httpd.server_close()


class SimpleServe(ThreadingMixIn, TCPServer):
    allow_reuse_address = True


class SimpleRequests(SimpleHTTPRequestHandler):
    def send_head(self):
        path = self.translate_path(self.path)

        f = None
        if os.path.isdir(path):
            if not self.path.endswith("/"):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            # else:
            #   return self.list_directory(path)

        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            print("%s" % path)
            f = open(path, "rb")

        except IOError:
            self.send_error(404, "File not found")
            return None

        fs = os.fstat(f.fileno())
        tp = self.guess_type(path)

        headers = {"Content-type": tp, "Content-Length": str(fs[6]), "Cache-Control": "no-cache, must-revalidate"}

        # Last-Modified", self.date_time_string(fs.st_mtime)

        return self.send_content(200, headers, f)

    def send_content(self, code, headers, file_handler):

        self.send_response(code)

        for key, value in headers.iteritems():
            self.send_header(key, value)

        self.end_headers()

        return file_handler

    def log_message(self, format, *args):
        sys.stdout.write("%s\n" % format % args)

    def log_request(self, code="", size=""):
        try:
            self.log_message("%s %s %s", str(code), self.requestline.split(" ")[0], self.requestline.split(" ")[1])
        except Exception:
            pass

    def guess_type(self, path):
        mimetype, encoding = mimetypes.guess_type(path)
        return mimetype if mimetype else "text/html"
