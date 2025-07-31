from flask import Flask, render_template, request, redirect, url_for, jsonify
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

# New ATS Score route
@app.route('/ats-score')
def ats_score():
    file_param = request.args.get('file')
    enhanced_param = request.args.get('enhanced')
    return render_template('ats-score.html', file=file_param, enhanced=enhanced_param)

# API endpoint for ATS analysis (for future Gemini integration)
@app.route('/api/analyze-ats', methods=['POST'])
def analyze_ats():
    try:
        data = request.get_json()
        file_name = data.get('fileName')
        session_id = data.get('sessionId')
        
        # TODO: Implement Gemini LLM analysis here
        # For now, return mock data
        mock_results = {
            'overallScore': 78,
            'breakdown': [
                {'category': 'Keywords Match', 'score': 82, 'description': 'Good keyword optimization'},
                {'category': 'Format Compatibility', 'score': 90, 'description': 'Excellent ATS-friendly format'},
                {'category': 'Section Organization', 'score': 75, 'description': 'Well-structured sections'},
                {'category': 'Contact Information', 'score': 95, 'description': 'Complete contact details'},
                {'category': 'Skills Alignment', 'score': 65, 'description': 'Some skills could be better highlighted'}
            ],
            'recommendations': [
                'Add more industry-specific keywords in your experience section',
                'Include quantifiable achievements with numbers and percentages',
                'Ensure consistent formatting throughout the document',
                'Add a skills section with relevant technical competencies'
            ]
        }
        
        return jsonify(mock_results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)