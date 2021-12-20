import os
 
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
 
 
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
 
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB
 
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
 
@app.route('/')
def upload_form(): # controller
    return render_template('upload.html') # view
# no model
 
 
@app.route('/', methods=['POST']) # 127.0.0.1:5000/ 
def upload_image(): # controller
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url) # view
 
    file = request.files['file']
 
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url) # view
 
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # model
        flash('Image successfully uploaded and displayed below')
        return render_template('upload.html', filename=filename) # view
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url) # view
 
 
@app.route('/display/<filename>')
def display_image(filename): # Controller
    return redirect(url_for('static', filename='uploads/' + filename), code=301) # View/Model
 
 
if __name__ == "__main__":
    app.run(debug=True)