import requests
import base64
import json
from flask import Flask, render_template

app = Flask(__name__)

FIND_FACES_SERVER_URL = 'http://localhost:5000/find_face'
IMG_URL = "http://localhost:8000/igor-1.jpg"


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/find_face')
def find_face():
    return render_template('find_face_post.html')


@app.route('/find_face_post', methods=['POST'])
def find_face_post():
    img_url = IMG_URL
    # Get image
    img = requests.get(img_url).content

    # Get coords from server-helper. Sends img in base64 string
    response = requests.post(FIND_FACES_SERVER_URL,
                             data={'img': base64.b64encode(img)})

    # Get json response
    json_data = json.loads(response.text)

    # Parse json
    face_locations = json_data.get('coordinates', [])

    # Render template
    return render_template('find_face_template.html',
                           img=img_url,
                           coordinates=face_locations)


if __name__ == '__main__':
    app.run(port=8888)
