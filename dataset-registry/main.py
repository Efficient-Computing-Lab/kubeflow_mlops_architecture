from flask import Flask, send_file, abort, request
from werkzeug.utils import safe_join
import os
import logging
import zipfile

app = Flask(__name__)

directory = os.environ.get('ENV_PATH', '/home/giannis')


# Option 1: Using send_file
@app.route('/download/<model>', methods=['GET'])
def download_file(model):
    # Define the path to the directory where the files are stored

    # Create the full file path
    folder_path = os.path.join(directory, model)
    find_file=""
    for file_name in os.listdir(folder_path):
        # Check if the file ends with '.zip'
        if file_name.endswith('.zip'):
            find_file = os.path.join(folder_path, file_name)
    try:
        # Send the file to the client
        return send_file(find_file, as_attachment=True)
    except FileNotFoundError:
        # Return a 404 error if the file is not found
        abort(404)


@app.route('/upload/', methods=['POST'])
def upload_file():
    # Check if the POST request contains a file
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']

    # Check if the file is empty
    if file.filename == '':
        return 'No selected file', 400
        # Get model_name from the request form data
    model_name = request.form.get('model_name')
    if not model_name:
        return 'No model_name provided', 400
    models_path = directory+"/"+model_name
    if not os.path.exists(models_path):
        os.makedirs(models_path)
    # Save the file to a local directory with its original filename
    file.save(os.path.join(models_path, file.filename))

    return 'File uploaded successfully', 200


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4422)
