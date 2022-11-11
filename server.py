# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import stableDiffusion2
import urllib.parse
import json


hostName = "0.0.0.0"
# hostName = "localhost"
serverPort = 6969
imggen = stableDiffusion2.theAlgo()

class MyServer(BaseHTTPRequestHandler):
    protocol_version: str = 'HTTP/1.1'
    def do_GET(self):
        try:

            givenPath = self.path.split("/")[2]
            decodedURL = urllib.parse.unquote(givenPath)
            imgLocation= imggen.generate(decodedURL)
            # self.send_response(200)
            
            self.send_header("Content-type", "application/json")
            self.send_header("Content-Length", len(imgLocation))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_response(code=200)
            self.end_headers()
            self.wfile.write(json.dump( {"filePath":imgLocation}))
            print(imgLocation, '\n\n')
        except:
            self.send_error(500,"there was an error")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
