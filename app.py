from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
from fr import get_encoded_faces, unknown_image_encoded, classify_face



app=Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["IMAGE_UPLOADS"] = UPLOAD_FOLDER
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False




@app.route('/faces/<string:name>')
def faces(name):
    return render_template('faces.html', face=name)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=='POST':        
        if request.files:

            image = request.files["image"]

            if image.filename == "":
                print("No filename")
                return redirect(request.url)

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)

                image.save(os.path.join('static/'+app.config["IMAGE_UPLOADS"], filename))

                print("Image saved")
                im, name=classify_face('static\\uploads\\'+filename)
                return redirect('/faces/'+name)
        else:
            print('no image')
        return redirect('/')
    return render_template('index.html')
    

if __name__=="__main__":
    get_encoded_faces()
    app.run(debug=True)