import os
from flask import Flask
from flask import jsonify

app = Flask(__name__)

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", use_reloader=False)