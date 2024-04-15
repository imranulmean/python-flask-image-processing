from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# app instance
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'  # Define the folder where uploaded files are stored
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# /api/home
# @app.route("/api/home", methods=['GET'])
# def return_home():
#     return jsonify({
#         'message': "Like this video if this helped!",
#         'people': ['Jack', 'Harry', 'Arpan']
#     })

@app.route("/api/home",methods=["GET"])
def test():
    a="hello world"
    return jsonify(a)

@app.route('/api/upload', methods=['POST'])
def upload():       
       if 'photo' not in request.files:
        return {'error': 'No file part'}, 400

       file = request.files['photo']
       print(file.filename) 
       if file.filename == '':
        return {'error': 'No selected file'}, 400

       file.save('uploads/' + file.filename)
       return jsonify({
           "msg":"File Uploaded Succecfully",
           "fileName": file.filename

       })

# Route to serve download files
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True, port=8080)