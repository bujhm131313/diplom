import os
import base64
import io
from flask import Flask, request, redirect, url_for, flash, send_file, render_template
from werkzeug.utils import secure_filename
# from gallery import *
from gallery import gallery

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/gallery', methods=['GET'])
def show_gallery():
    photos = gallery.gallery_get_all()
    photos_b64 = []
    for photo in photos:
        photo_b64 = base64.b64encode(photo.getvalue()).decode()
        photos_b64.append(photo_b64)

    return render_template('images.html', images=photos_b64)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.seek(0, os.SEEK_END)
            file_length = file.tell()
            file.seek(0)
            gallery_put(filename, file, file_length)
            return redirect(request.url)

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

html = '''
<html>
    <body>
        <img src="data:image/png;base64,{}" />
    </body>
</html>
'''

@app.route('/test', methods=['GET', 'POST'])
def tupload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(type(file))
            image = io.BytesIO(file.read())
            data = base64.b64encode(image.getvalue()).decode()

            return html.format(data)
            # return send_file(image, mimetype='image/png')

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(port=9999, debug=True)