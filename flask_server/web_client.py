import requests
import base64
import json
import os
from flask import Flask, render_template, request, send_from_directory
from flask_oidc import OpenIDConnect
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_USER_INFO_ENABLED': True,
    'OIDC_OPENID_REALM': 'flask-demo',
    'OIDC_SCOPES': ['openid', 'email', 'profile'],
    'OIDC_INTROSPECTION_AUTH_METHOD': 'client_secret_post'
})

oidc = OpenIDConnect(app)


VERIFY_FACES_SERVER_URL = 'http://localhost:5000/verify_face'
FIND_FACES_SERVER_URL = 'https://localhost:8443/apiman-gateway/FaceAPI/faceapi/v1/'
IMG_URL = "http://localhost:8000/igor-1.jpg"
UPLOAD_FOLDER = './uploads'


def authorize():
    token = requests.post(
        'http://127.0.0.1:8080/auth/realms/faceapi/protocol/openid-connect/token',
        headers={
            "Content-Type": "application/x-www-form-urlencoded"},
        data={
            'username': 'faceapiuser',
            'password': 'faceapiuser',
            'grant_type': 'password',
            'client_id': 'apiman',
        })
    json_web_token = token.json().get('access_token', False)
    return json_web_token


@app.route('/')
def hello_world():
    if oidc.user_loggedin:
        return ('Hello, %s, <a href="/private">See private</a> '
                '<a href="/logout">Log out</a>') % \
               oidc.user_getfield('preferred_username')
    else:
        return 'Welcome anonymous, <a href="/private">Log in</a>'


@app.route('/private')
@oidc.require_login
def hello_me():
    """Example for protected endpoint that extracts private information from the OpenID Connect id_token.
       Uses the accompanied access_token to access a backend service.
    """

    info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])

    username = info.get('preferred_username')
    email = info.get('email')
    user_id = info.get('sub')

    if user_id in oidc.credentials_store:
        try:
            from oauth2client.client import OAuth2Credentials
            access_token = OAuth2Credentials.from_json(
                oidc.credentials_store[user_id]).access_token
            print
            'access_token=<%s>' % access_token
            headers = {'Authorization': 'Bearer %s' % (access_token)}
            # YOLO
            greeting = requests.get('http://localhost:8080/greeting',
                                    headers=headers).text
        except:
            print
            "Could not access greeting-service"
            greeting = "Hello %s" % username

    return ("""%s your email is %s and your user_id is %s!
               <ul>
                 <li><a href="/">Home</a></li>
                 <li><a href="//localhost:8081/auth/realms/pysaar/account?referrer=flask-app&referrer_uri=http://localhost:5000/private&">Account</a></li>
                </ul>""" %
            (greeting, email, user_id))


@app.route('/find_face')
def find_face():
    return render_template('find_face_post.html')


@app.route('/verify_face')
def verify_face():
    return render_template('verify_face_post.html')


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

        json_web_token = authorize()
        response = requests.post(FIND_FACES_SERVER_URL + 'find_face',
                                 verify=False,
                                 headers={'Authorization': 'Bearer {}'.format(
                                     json_web_token)},
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


@app.route('/verify_face_post', methods=['POST'])
def verify_face_post():

    known_img = request.files.get('known_img', False)
    unknown_img = request.files.get('unknown_img', False)

    if known_img and unknown_img:

        base64_known_img = base64.b64encode(known_img.read())
        base64_unknown_img = base64.b64encode(unknown_img .read())

        # json_web_token = authorize()
        response = requests.post(VERIFY_FACES_SERVER_URL,
                                 verify=False,
                                 data={'known_img': base64_known_img,
                                       'unknown_img': base64_unknown_img
                                       })

        return render_template('verify_face_template.html',
                               result=response.content.decode('utf-8') == 'True')
    else:
        return "Upload img, plz"


if __name__ == '__main__':
    app.run(port=8888)
