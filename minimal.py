import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import melody_extraction as me

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = set(['txt', 'csv', 'wav', 'mp3', 'flac'])
processed = False
default = """

"""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def processed_answer():
    if processed:
        return processed
    else:
        return "Need to implement"
    

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # r = request.files['range']
        # c = request.files['checkbox']
        print(request)
        op = request.form.get("open_string", None)
        sp = request.form['string_penalty']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("index.html", output=me.launcher(filename, sp, op))        
    return render_template("index.html", output=False)

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

