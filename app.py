from flask import Flask, render_template, request, jsonify, send_file, Response
import os
from werkzeug.utils import secure_filename
from utils.document_processor import process_document
from utils.summarizer import generate_summary
from utils.text_to_speech import generate_audio
from dotenv import load_dotenv
import threading
import json

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH'))

ALLOWED_EXTENSIONS = {'pdf', 'docx'}
processing_status = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(file_id, filepath):
    try:
        # Update status
        processing_status[file_id] = {'status': 'processing', 'step': 'extracting_text', 'progress': 0}
        text = process_document(filepath)
        
        processing_status[file_id] = {'status': 'processing', 'step': 'summarizing', 'progress': 33}
        summary = generate_summary(text)
        
        processing_status[file_id] = {'status': 'processing', 'step': 'generating_audio', 'progress': 66}
        audio_path = generate_audio(summary)
        
        processing_status[file_id] = {
            'status': 'completed',
            'progress': 100,
            'summary': summary,
            'audio_path': audio_path
        }
    except Exception as e:
        processing_status[file_id] = {'status': 'error', 'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Generate unique ID for this process
        file_id = str(hash(filename + str(os.path.getsize(filepath))))
        
        # Start processing in background
        thread = threading.Thread(target=process_file, args=(file_id, filepath))
        thread.start()
        
        return jsonify({'file_id': file_id})
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/status/<file_id>')
def get_status(file_id):
    return jsonify(processing_status.get(file_id, {'status': 'not_found'}))

@app.route('/audio/<filename>')
def get_audio(filename):
    return send_file(f"uploads/{filename}", mimetype="audio/mp3")

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)