import requests
import io
from flask import Flask, render_template

from face_recognition_utils import utils

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/find_face')
def find_face():
    img_url = "http://localhost:8000/igor-1.jpg"

    img = io.BytesIO(requests.get(img_url).content)
    face_locations = utils.get_face_coordinates(img)
    return render_template('find_face_template.html',
                           img=img_url,
                           coordinates=face_locations)


if __name__ == '__main__':
    app.run()
