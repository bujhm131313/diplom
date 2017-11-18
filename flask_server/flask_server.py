from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/find_face')
def find_face():
    return 'YOUR FACE'


if __name__ == '__main__':
    app.run()
