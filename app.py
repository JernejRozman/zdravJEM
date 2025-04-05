from flask import Flask

a = Flask(__name__)

@a.route('/')
def hello_world():
    return 'Hello, World!'