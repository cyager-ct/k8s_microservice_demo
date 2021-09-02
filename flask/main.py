import os
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)