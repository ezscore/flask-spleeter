import os
import shutil
from flask import Flask, render_template, request, send_file, after_this_request
from spleeter.separator import Separator
from werkzeug.utils import secure_filename
import warnings
warnings.filterwarnings('ignore')

# @misc{spleeter2019,
#   title={Spleeter: A Fast And State-of-the Art Music Source Separation Tool With Pre-trained Models},
#   author={Romain Hennequin and Anis Khlif and Felix Voituret and Manuel Moussallam},
#   howpublished={Late-Breaking/Demo ISMIR 2019},
#   month={November},
#   note={Deezer Research},
#   year={2019}
#

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__)) #flask-spleeter

def separate_file(mp3_file, destination):
    separator = Separator('spleeter:2stems')
    print(mp3_file, destination)
    print('this is where it fails')
    separator.separate_to_file(mp3_file, destination)

@app.route("/")
def index():
    return render_template('upload.html')

@app.route("/upload", methods=['POST', 'GET'])
def upload():

    target = APP_ROOT #flask-spleeter
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(target, filename)) #flask-spleeter/filename
    separate_file(filename, target)

    path_to_file = target + '/' + filename.strip('.mp3') + '/' + 'vocals.wav' #the path for the relevant files (vocals)

    #Delete file after processing
    @after_this_request
    def remove_file(response):
        try:
            os.remove(target+"/"+filename)
            shutil.rmtree(target+"/"+filename.strip('.mp3'))
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response
    return send_file(
        path_to_file,
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename="vocal.wav")

if __name__ == "__main__":
    app.run(port=4555, debug=True)
