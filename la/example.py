from flask import Flask

app = Flask(__name__)


@app.route('/')
def route():
    return "Hello, Learning Analytics!"
