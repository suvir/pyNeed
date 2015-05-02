import os
from app import app

port = os.getenv('VCAP_APP_PORT', 8000)

# For local usage
app.run(debug=True)
# For bluemix
# app.run(host='0.0.0.0', port=int(port))

# ORIGINAL FLASK TUTORIAL CODE 
# import os
# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def hello():
#     return 'Hello World!'

# port = os.getenv('VCAP_APP_PORT', 8000)

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=int(port))

# ORIGINAL STARTER CODE:
# import os
# try:
#   from SimpleHTTPServer import SimpleHTTPRequestHandler as Handler
#   from SocketServer import TCPServer as Server
# except ImportError:
#   from http.server import SimpleHTTPRequestHandler as Handler
#   from http.server import HTTPServer as Server

# # Read port selected by the cloud for our application
# PORT = int(os.getenv('VCAP_APP_PORT', 8000))
# # Change current directory to avoid exposure of control files
# os.chdir('static')

# httpd = Server(("", PORT), Handler)
# try:
#   print("Start serving at port %i" % PORT)
#   httpd.serve_forever()
# except KeyboardInterrupt:
#   pass
# httpd.server_close()

