import io
from flask import Flask, request, jsonify
import base64

from face_recognition_utils import utils

app = Flask(__name__)


@app.route('/find_face', methods=['POST'])
def find_face():

    """
    Finds face coords. Takes img(string of base64) from request params
    :return: face coords
    """
    # Get image from params
    img = request.form.get('img', False)

    # Convert image from string to base64
    base64_img = base64.b64decode(img)
    if img:
        # Find locations
        face_locations = utils.get_face_coordinates(io.BytesIO(base64_img))

        # Return json
        return jsonify(coordinates=face_locations)
    else:
        return "400"


if __name__ == '__main__':
    app.run()
