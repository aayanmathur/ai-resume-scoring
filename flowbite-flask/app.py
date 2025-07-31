from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/resume-options')
def resume_options():
    return render_template('resume-options.html')

@app.route('/upload-resume', methods=['GET'])
def upload_resume():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('resume')
    if file:
        # Example: read contents (in memory)
        content = file.read()  # bytes
        filename = file.filename
        # You can parse `content` here using your resume parser logic
        print(f"Uploaded: {filename}, size: {len(content)} bytes")
        return 'Upload processed in memory!'
    return 'No file uploaded!', 400

@app.route('/templates.html')
def templates():
    return render_template('templates.html')

@app.route('/download.html')
def download():
    session_id = request.args.get('session')
    return render_template('download.html', session=session_id)

@app.route('/build-resume', methods=['GET'])
def build_resume():
    return render_template('build-resume.html')


if __name__ == '__main__':
    app.run(debug=True)