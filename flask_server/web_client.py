import requests
import base64
import json
import os
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

FIND_FACES_SERVER_URL = 'http://localhost:5000/find_face'
IMG_URL = "http://localhost:8000/igor-1.jpg"
UPLOAD_FOLDER = './uploads'


@app.route('/')
def hello_world():
    return render_template('layout.html')


@app.route('/find_face')
def find_face():
    return render_template('find_face_post.html')


@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)


@app.route('/find_face_post', methods=['POST'])
def find_face_post():

    img = request.files.get('file', False)

    if img:

        filename = secure_filename(img.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        img.save(file_path)

        # It's kinda strange, but there is a pointer in image reader and we
        # need to point it to the start again after previous reading
        img.seek(0)

        base64_img = base64.b64encode(img.read())
        # Get coords from server-helper. Sends img in base64 string
        response = requests.post(FIND_FACES_SERVER_URL,
                                 data={'img': base64_img})

        # Get json response
        json_data = json.loads(response.text)

        # Parse json
        face_locations = json_data.get('coordinates', [])

        # Render template
        return render_template('find_face_template.html',
                               image=filename,
                               coordinates=face_locations)
    else:
        return "Upload img, plz"


if __name__ == '__main__':
    app.run(port=8888)
