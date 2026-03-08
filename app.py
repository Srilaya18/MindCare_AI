from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import re

app = Flask(__name__)

def clean_text(text):
    """Remove special characters and extra spaces to preprocess text."""
    return re.sub(r'[^a-zA-Z\s]', '', text)

def analyze_stress(text):
    """
    Perform natural language processing to detect emotional intensity.
    Uses polarity to determine stress level.
    """
    cleaned = clean_text(text)
    blob = TextBlob(cleaned)
    polarity = blob.sentiment.polarity
    
    # Classification rules for stress levels
    if polarity < -0.2:
        return "HIGH", "It sounds like you are experiencing significant stress. Taking breaks, practicing relaxation techniques, or talking to someone you trust may help."
    elif polarity < 0.2:
        return "MEDIUM", "You seem to be carrying some tension. Remember to take a deep breath, and maybe take a short walk or listen to some calming music."
    else:
        return "LOW", "You seem to be in a relatively good or balanced space. Keep up the positive habits!"

@app.route('/')
def home():
    """Serve the single-page application interface."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """API endpoint to receive text, perform sentiment analysis, and return support response."""
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400
        
    text = data['text']
    stress_level, message = analyze_stress(text)
    
    response = {
        'stress_level': stress_level,
        'message': message,
        'resources': [
            {'name': 'National Mental Health Helpline', 'contact': '9152987821'},
            {'name': 'Student Counseling Center', 'contact': 'Reach out to your campus counseling center'}
        ],
        'tips': [
            'Practice 4-7-8 breathing',
            'Take a 15-minute walk outside',
            'Maintain a consistent sleep schedule',
            'Talk to a trusted friend or family member'
        ]
    }
    return jsonify(response)

if __name__ == '__main__':
    # Run server locally (Config item constraint execution)
    app.run(debug=True, port=5000)
