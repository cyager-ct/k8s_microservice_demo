import os
import requests
from flask import jsonify, request, Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Welcome to our flask app</h1>"

@app.route("/health")
def health_check():
    '''
	health check function
    '''
    return "OK"

@app.route("/ip_address")
def ip_address():
    ip = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4").content
    return ip

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)