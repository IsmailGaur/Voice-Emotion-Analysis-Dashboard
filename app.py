from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from audio_processing.preprocess import AudioProcessor
from emotion_model.model import EmotionDetector
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'flac', 'ogg', 'm4a'}

# Initialize processors
audio_processor = AudioProcessor()
emotion_detector = EmotionDetector()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/analyze', methods=['POST'])
def analyze_audio():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Allowed: wav, mp3, flac, ogg, m4a'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process audio
        chunks = audio_processor.process_audio(filepath)
        
        # Detect emotions for each chunk
        results = []
        for chunk in chunks:
            emotion_data = emotion_detector.predict_emotion(
                chunk['audio_data'],
                chunk['sample_rate']
            )
            
            results.append({
                'start_time': chunk['start_time'],
                'end_time': chunk['end_time'],
                'emotion': emotion_data['emotion'],
                'confidence': emotion_data['confidence'],
                'all_scores': emotion_data['scores']
            })
        
        # Detect emotion changes
        emotion_changes = detect_emotion_changes(results)
        
        # Calculate statistics
        stats = calculate_statistics(results)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'results': results,
            'emotion_changes': emotion_changes,
            'statistics': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def detect_emotion_changes(results):
    """Detect when emotions change between chunks"""
    changes = []
    
    if len(results) < 2:
        return changes
    
    previous_emotion = results[0]['emotion']
    
    for i in range(1, len(results)):
        current_emotion = results[i]['emotion']
        
        if current_emotion != previous_emotion:
            changes.append({
                'timestamp': results[i]['start_time'],
                'from_emotion': previous_emotion,
                'to_emotion': current_emotion,
                'confidence': results[i]['confidence']
            })
            previous_emotion = current_emotion
    
    return changes

def calculate_statistics(results):
    """Calculate emotion distribution and statistics"""
    emotion_counts = {}
    emotion_durations = {}
    total_duration = 0
    
    for result in results:
        emotion = result['emotion']
        duration = result['end_time'] - result['start_time']
        
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        emotion_durations[emotion] = emotion_durations.get(emotion, 0) + duration
        total_duration += duration
    
    # Calculate percentages
    emotion_percentages = {
        emotion: (duration / total_duration * 100) if total_duration > 0 else 0
        for emotion, duration in emotion_durations.items()
    }
    
    # Find dominant emotion
    dominant_emotion = max(emotion_durations.items(), key=lambda x: x[1])[0] if emotion_durations else 'Unknown'
    
    return {
        'total_duration': round(total_duration, 2),
        'emotion_counts': emotion_counts,
        'emotion_durations': {k: round(v, 2) for k, v in emotion_durations.items()},
        'emotion_percentages': {k: round(v, 2) for k, v in emotion_percentages.items()},
        'dominant_emotion': dominant_emotion
    }

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
