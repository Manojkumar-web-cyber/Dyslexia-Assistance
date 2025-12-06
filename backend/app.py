from flask import Flask, request, jsonify, send_from_directory  # ← ADD send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
import logging


# Import custom modules
from modules.speech_analysis import SpeechAnalyzer
from modules.attention_tracking import AttentionTracker
from modules.difficulty_adapter import DifficultyAdapter
from modules.multisensory_support import MultisensorySupportEngine
from modules.mentor_persona import MentorPersona


load_dotenv()
app = Flask(__name__)
# Allow all origins and credentials
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Initialize AI modules
speech_analyzer = SpeechAnalyzer()
attention_tracker = AttentionTracker()
difficulty_adapter = DifficultyAdapter()
support_engine = MultisensorySupportEngine()
mentor_persona = MentorPersona()


# Global session data
session_data = {
    'reading_history': [],
    'performance_metrics': {},
    'engagement_data': [],
    'error_patterns': {}
}


# ============= FRONTEND ROUTES =============

@app.route('/')
def index():
    """Serve frontend index.html"""
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '../frontend'), 'index.html')
    except Exception as e:
        return "Frontend not found", 404

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve frontend static files (CSS, JS, images)"""
    try:
        return send_from_directory(os.path.join(os.path.dirname(__file__), '../frontend'), filename)
    except Exception as e:
        return f"File not found: {filename}", 404

# ==============================================


@app.route('/health', methods=['GET'])
def health():
    print(" /health endpoint was hit")
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/analyze-speech', methods=['POST'])
def analyze_speech():
    print(" /api/analyze-speech endpoint was hit")
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        expected_text = request.form.get('expected_text', '')
        
        transcription = speech_analyzer.transcribe(audio_file)
        analysis = speech_analyzer.analyze_pronunciation(transcription, expected_text)
        
        session_data['reading_history'].append(analysis)
        
        return jsonify({
            'transcription': transcription,
            'analysis': analysis,
            'accuracy': analysis.get('accuracy_score', 0)
        }), 200
        
    except Exception as e:
        logger.error(f"Speech analysis error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/track-attention', methods=['POST'])
def track_attention():
    print(" /api/track-attention endpoint was hit")
    try:
        if 'frame' not in request.files:
            return jsonify({'error': 'No frame provided'}), 400
        
        frame_file = request.files['frame']
        attention_metrics = attention_tracker.analyze_frame(frame_file)
        session_data['engagement_data'].append(attention_metrics)
        
        return jsonify({
            'gaze_direction': attention_metrics['gaze_direction'],
            'blink_rate': attention_metrics['blink_rate'],
            'focus_level': attention_metrics['focus_level'],
            'engagement_score': attention_metrics['engagement_score'],
            'fatigue_detected': attention_metrics['fatigue_detected']
        }), 200
        
    except Exception as e:
        logger.error(f"Attention tracking error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/get-support', methods=['POST'])
def get_support():
    print(" /api/get-support endpoint was hit")
    try:
        data = request.get_json()
        text = data.get('text', '')
        support_type = data.get('support_type', 'all')
        
        support = support_engine.generate_support(text=text, support_type=support_type)
        
        return jsonify({
            'text_to_speech_url': support.get('tts_url'),
            'visual_cues': support.get('visual_cues'),
            'hints': support.get('hints'),
            'syllable_breakdown': support.get('syllable_breakdown')
        }), 200
        
    except Exception as e:
        logger.error(f"Support generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/get-mentor-feedback', methods=['POST'])
def get_mentor_feedback():
    print(" /api/get-mentor-feedback endpoint was hit")
    try:
        data = request.get_json()
        feedback = mentor_persona.generate_feedback(
            reading_history=session_data['reading_history'],
            performance_data=data.get('performance_data', {}),
            engagement_data=session_data['engagement_data'],
            error_patterns=session_data['error_patterns'],
            learner_age=data.get('learner_age', 'teen'),
            personality_preference=data.get('personality', 'friendly')
        )
        
        return jsonify({
            'encouragement': feedback['encouragement'],
            'insights': feedback['insights'],
            'recommendations': feedback['recommendations'],
            'session_summary': feedback['session_summary'],
            'next_steps': feedback['next_steps']
        }), 200
        
    except Exception as e:
        logger.error(f"Mentor feedback error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/end-session', methods=['POST'])
def end_session():
    print(" /api/end-session endpoint was hit")
    try:
        summary = mentor_persona.generate_session_summary(
            reading_history=session_data['reading_history'],
            engagement_data=session_data['engagement_data']
        )
        
        session_data['reading_history'] = []
        session_data['engagement_data'] = []
        
        return jsonify(summary), 200
        
    except Exception as e:
        logger.error(f"Session end error: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
