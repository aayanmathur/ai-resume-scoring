from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document
import magic
import re
import traceback
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Setup
app = Flask(__name__)
load_dotenv()

# Debug: Check if API key is loaded
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("GEMINI_API_KEY not found in environment variables")
else:
    logger.info(f"GEMINI_API_KEY loaded: {api_key[:10]}...")
    genai.configure(api_key=api_key)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Routes
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
    try:
        logger.info("Upload request received")
        
        if 'resume' not in request.files:
            logger.error("No file in request")
            return jsonify({'error': 'No file uploaded'}), 400
            
        file = request.files['resume']
        
        if file.filename == '':
            logger.error("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
            
        if file:
            original_filename = file.filename
            secured_filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], secured_filename)
            
            # Make sure uploads directory exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            file.save(path)
            logger.info(f"File saved as: {secured_filename} (original: {original_filename})")
            
            # Return the secured filename so frontend knows what was actually saved
            return jsonify({
                'success': True, 
                'filename': secured_filename,
                'originalName': original_filename
            }), 200
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'Upload failed'}), 500


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

@app.route('/ats-score')
def ats_score():
    file_param = request.args.get('file')
    enhanced_param = request.args.get('enhanced')
    return render_template('ats-score.html', file=file_param, enhanced=enhanced_param)

@app.route('/api/analyze-ats', methods=['POST'])
def analyze_ats():
    try:
        logger.info("ATS analysis request received")
        
        # Get request data
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data provided'}), 400
            
        file_name = data.get('fileName')
        if not file_name:
            logger.error("No fileName in request data")
            return jsonify({'error': 'No file name provided'}), 400
            
        logger.info(f"Analyzing file: {file_name}")

        # Ensure uploads directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Check if file exists
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            # List files in directory for debugging
            try:
                files = os.listdir(app.config['UPLOAD_FOLDER'])
                logger.info(f"Files in upload directory: {files}")
            except:
                logger.error("Could not list upload directory")
            return jsonify({'error': 'File not found on server'}), 404

        # Extract text from file
        logger.info("Extracting text from file")
        resume_text = extract_text(file_path)
        
        if not resume_text or resume_text == 'Unsupported file type':
            logger.error(f"Failed to extract text from file: {file_name}")
            return jsonify({'error': 'Could not extract text from file'}), 400
            
        logger.info(f"Extracted text length: {len(resume_text)} characters")

        # Check if Gemini is configured
        if not api_key:
            logger.error("Gemini API key not configured")
            return jsonify(get_mock_data())

        # Create prompt for Gemini
        prompt = f"""
You are an ATS (Applicant Tracking System) analysis expert. 
Analyze the following resume text and provide a structured response in the exact format below:

OVERALL ATS COMPATIBILITY SCORE: [number from 0-100]

BREAKDOWN:
Keywords Match: [score 0-100] - [brief description]
Format Compatibility: [score 0-100] - [brief description]  
Section Organization: [score 0-100] - [brief description]
Contact Information: [score 0-100] - [brief description]
Skills Alignment: [score 0-100] - [brief description]

RECOMMENDATIONS:
1. [specific improvement recommendation]
2. [specific improvement recommendation]
3. [specific improvement recommendation]
4. [specific improvement recommendation]
5. [specific improvement recommendation]

Resume Text:
{resume_text[:3000]}
"""

        logger.info("Sending request to Gemini")
        
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            
            if not response or not response.text:
                raise Exception("Empty response from Gemini")
                
            logger.info("Received response from Gemini")
            logger.debug(f"Gemini response: {response.text[:500]}...")
            
            # Parse the response
            parsed = parse_gemini_output(response.text)
            logger.info(f"Parsed response successfully")
            
            return jsonify(parsed)
            
        except Exception as gemini_error:
            logger.error(f"Gemini API error: {str(gemini_error)}")
            logger.info("Falling back to mock data")
            return jsonify(get_mock_data())

    except Exception as e:
        logger.error(f"General error in analyze_ats: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# Helpers
def extract_text(file_path):
    try:
        logger.info(f"Extracting text from: {file_path}")
        
        # Get file mime type
        mime = magic.Magic(mime=True).from_file(file_path)
        logger.info(f"File mime type: {mime}")
        
        if mime == 'application/pdf':
            logger.info("Processing PDF file")
            reader = PdfReader(file_path)
            text = '\n'.join([p.extract_text() or '' for p in reader.pages])
            logger.info(f"Extracted PDF text length: {len(text)}")
            return text
            
        elif mime in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
            logger.info("Processing Word document")
            doc = Document(file_path)
            text = '\n'.join([p.text for p in doc.paragraphs])
            logger.info(f"Extracted Word text length: {len(text)}")
            return text
        else:
            logger.error(f"Unsupported file type: {mime}")
            return 'Unsupported file type'
            
    except Exception as e:
        logger.error(f"Error extracting text: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return 'Error extracting text'

def parse_gemini_output(text):
    try:
        logger.info("Parsing Gemini output")
        
        # Extract overall score
        score_patterns = [
            r'OVERALL ATS COMPATIBILITY SCORE:\s*(\d+)',
            r'Overall.*?score.*?(\d+)',
            r'Score.*?(\d+)',
        ]
        
        overall_score = 70  # default
        for pattern in score_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                overall_score = int(match.group(1))
                break
        
        logger.info(f"Extracted overall score: {overall_score}")

        # Extract breakdown
        breakdown = []
        categories = ['Keywords Match', 'Format Compatibility', 'Section Organization', 'Contact Information', 'Skills Alignment']
        
        for cat in categories:
            # Try multiple patterns for each category
            patterns = [
                rf'{cat}:\s*(\d+)\s*-\s*(.+?)(?:\n|$)',
                rf'{cat}.*?(\d+).*?-\s*(.+?)(?:\n|$)',
                rf'{cat}.*?(\d+)\s*(.+?)(?:\n|$)',
            ]
            
            found = False
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
                if match:
                    score = int(match.group(1))
                    description = match.group(2).strip()[:100]  # Limit description length
                    breakdown.append({
                        'category': cat,
                        'score': min(100, max(0, score)),  # Ensure score is 0-100
                        'description': description
                    })
                    found = True
                    break
            
            # If no match found, add default
            if not found:
                breakdown.append({
                    'category': cat,
                    'score': overall_score + (-10 + len(breakdown) * 5),  # Vary scores around overall
                    'description': f'Analysis for {cat.lower()}'
                })

        logger.info(f"Extracted breakdown: {len(breakdown)} items")

        # Extract recommendations
        recommendations = []
        
        # Try to find numbered recommendations
        rec_matches = re.findall(r'(?:^|\n)\s*\d+\.\s*(.+?)(?=\n\d+\.|\n[A-Z]|\Z)', text, re.MULTILINE | re.DOTALL)
        
        if rec_matches:
            recommendations = [rec.strip() for rec in rec_matches[:5]]
        else:
            # Fallback: look for bullet points or lines after "RECOMMENDATIONS"
            rec_section = re.search(r'RECOMMENDATIONS:?\s*(.+)', text, re.IGNORECASE | re.DOTALL)
            if rec_section:
                lines = rec_section.group(1).split('\n')
                for line in lines[:5]:
                    line = line.strip()
                    if line and not line.startswith('Resume Text:'):
                        # Clean up the line
                        line = re.sub(r'^[-*•]\s*', '', line)
                        line = re.sub(r'^\d+\.\s*', '', line)
                        if len(line) > 10:  # Only include substantial recommendations
                            recommendations.append(line)
        
        # Ensure we have at least some recommendations
        if not recommendations:
            recommendations = [
                'Add more industry-specific keywords throughout your resume',
                'Use quantifiable achievements with specific numbers and metrics',
                'Ensure consistent formatting and clear section headers',
                'Include relevant technical skills in a dedicated skills section'
            ]

        logger.info(f"Extracted recommendations: {len(recommendations)} items")

        result = {
            'overallScore': overall_score,
            'breakdown': breakdown,
            'recommendations': recommendations[:5]  # Limit to 5 recommendations
        }
        
        logger.info("Successfully parsed Gemini output")
        return result
        
    except Exception as e:
        logger.error(f"Error parsing Gemini output: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        # Return fallback data
        return get_mock_data()

def get_mock_data():
    """Fallback mock data when Gemini fails"""
    return {
        'overallScore': 75,
        'breakdown': [
            {'category': 'Keywords Match', 'score': 70, 'description': 'Some relevant keywords present'},
            {'category': 'Format Compatibility', 'score': 85, 'description': 'Good ATS-friendly format'},
            {'category': 'Section Organization', 'score': 80, 'description': 'Well-structured sections'},
            {'category': 'Contact Information', 'score': 90, 'description': 'Complete contact details'},
            {'category': 'Skills Alignment', 'score': 65, 'description': 'Skills section needs improvement'}
        ],
        'recommendations': [
            'Add more industry-specific keywords in your experience section',
            'Include quantifiable achievements with numbers and percentages',
            'Ensure consistent formatting throughout the document',
            'Add a comprehensive skills section with relevant competencies',
            'Use action verbs to start bullet points in experience section'
        ]
    }

if __name__ == '__main__':
    app.run(debug=True)
