import requests
import io
import base64
import json
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/find_face')
def find_face():
    img_url = "http://localhost:8000/igor-1.jpg"
    img = requests.get(img_url).content

    response = requests.post('http://localhost:5000/find_face',
                             data={'img': base64.b64encode(img)})
    json_data = json.loads(response.text)
    face_locations = json_data.get('coordinates', [])
    return render_template('find_face_template.html',
                           img=img_url,
                           coordinates=face_locations)


if __name__ == '__main__':
    app.run(port=8888)
