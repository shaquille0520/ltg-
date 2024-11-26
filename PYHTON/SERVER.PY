from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Set the upload folder to a subfolder named 'uploads' in the script's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the HTML upload form
@app.route('/')
def upload_form():
    return render_template('upload.html')

# Route for handling file uploads and user data
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return "No files part", 400

    # Get user data
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    # Validate user data
    if not all([name, email, phone]):
        return "Please provide all required information.", 400

    files = request.files.getlist('files')
    saved_files = []

    for file in files:
        if file.filename == '':
            return "No selected file", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            saved_files.append(filename)
        else:
            return f"File '{file.filename}' is not allowed", 400

    # Construct response message with links to all uploaded files
    file_links = ''.join([f"<li><a href='/uploads/{filename}'>{filename}</a></li>" for filename in saved_files])
    response_html = f"""
        <h1>Upload Successful!</h1>
        <p>Thank you, {name}!</p>
        <p>Email: {email}<br>Phone: {phone}</p>
        <h2>Uploaded Files:</h2>
        <ul>{file_links}</ul>
    """
    return response_html, 200

# Route for viewing files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
	app.run()