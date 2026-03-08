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
    Extracts key topics from user text to tailor the response.
    """
    cleaned = clean_text(text)
    blob = TextBlob(cleaned)
    polarity = blob.sentiment.polarity
    words = cleaned.lower().split()
    
    # 1. Topic Extraction
    topic = "general"
    if any(word in words for word in ["exam", "exams", "study", "marks", "grade", "test"]):
        topic = "academic"
    elif any(word in words for word in ["sleep", "tired", "exhausted", "insomnia"]):
        topic = "sleep"
    elif any(word in words for word in ["lonely", "alone", "friend", "friends", "relationship"]):
        topic = "social"
    elif any(word in words for word in ["job", "work", "boss", "career"]):
        topic = "career"

    # 2. Dynamic Message Generation based on Polarity & Topic
    if polarity < -0.2:
        stress_level = "HIGH"
        if topic == "academic":
            message = "It sounds like your studies are putting an immense amount of pressure on you right now. It's incredibly common to feel overwhelmed by exams, but remember that a grade doesn't define your worth. Please prioritize taking a step back."
        elif topic == "sleep":
            message = "Sleep deprivation combined with stress is a vicious cycle. Your body and mind are exhausted. Please prioritize rest tonight and consider speaking to a professional."
        elif topic == "social":
            message = "Feeling isolated or struggling with relationships is profoundly difficult. You don't have to carry this alone. I strongly encourage you to reach out to one of the resources below."
        elif topic == "career":
            message = "Workplace stress can take over your entire life. It sounds like you are experiencing significant burnout. Setting strict boundaries and talking to someone may help."
        else:
            message = "It sounds like you are experiencing significant stress right now. Taking breaks, practicing relaxation techniques, or talking to someone you trust may help."

    elif polarity < 0.2:
        stress_level = "MEDIUM"
        if topic == "academic":
            message = "You seem to be carrying some tension regarding your academics. Break your study sessions into smaller, manageable chunks (like the Pomodoro technique) to avoid burning out."
        elif topic == "sleep":
            message = "You seem a bit fatigued. Practicing better sleep hygiene—like turning off screens an hour before bed—can help your mind wind down."
        elif topic == "social":
            message = "Navigating social dynamics can be draining. Remember to take time for yourself to recharge."
        elif topic == "career":
            message = "Work seems to be weighing on you. Remember to take your breaks and leave work at the door when you clock out."
        else:
            message = "You seem to be carrying some tension. Remember to take a deep breath, and maybe take a short walk or listen to some calming music."

    else:
        stress_level = "LOW"
        if topic == "academic":
            message = "You sound like you're in a good academic rhythm! Keep up the great study habits."
        elif topic == "sleep":
            message = "You sound rested and balanced. Good sleep is the foundation of a great mood!"
        elif topic == "social":
            message = "You sound like you're in a socially positive space right now. Enjoy those connections!"
        elif topic == "career":
            message = "It sounds like things are going smoothly at work. Keep up the positive momentum!"
        else:
            message = "You seem to be in a relatively good or balanced space. Keep up the positive habits!"

    return stress_level, message, topic

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
    stress_level, message, topic = analyze_stress(text)
    
    # 3. Dynamic Resources based on Topic
    resources = []
    if topic == "academic":
        resources = [
            {'name': 'University Academic Advising', 'contact': 'Visit your campus advising center'},
            {'name': 'Student Counseling Services', 'contact': 'Confidential campus support: 1-800-CAMPUS'}
        ]
    elif topic == "sleep":
        resources = [
            {'name': 'Sleep Foundation Helpline', 'contact': '1-800-SLEEP-WELL'},
            {'name': 'Local Sleep Clinic', 'contact': 'Consult your primary care physician'}
        ]
    elif topic == "social":
        resources = [
            {'name': 'Crisis Text Line', 'contact': 'Text HOME to 741741'},
            {'name': 'Community Support Groups', 'contact': 'Check local meetup boards for peer support'}
        ]
    elif topic == "career":
        resources = [
            {'name': 'Employee Assistance Program (EAP)', 'contact': 'Check with your HR department'},
            {'name': 'Career Counseling Center', 'contact': 'Local workforce development board'}
        ]
    else:
        resources = [
            {'name': 'National Mental Health Helpline', 'contact': '9152987821'},
            {'name': 'General Counseling Center', 'contact': 'Reach out to your local clinic'}
        ]

    # 4. Dynamic Tips based on Topic
    tips = []
    if topic == "academic":
        tips = [
            'Try the Pomodoro Technique (25 min study, 5 min break)',
            'Organize your notes into a daily to-do list',
            'Stay hydrated and avoid excessive caffeine',
            'Form a study group for peer support'
        ]
    elif topic == "sleep":
        tips = [
            'Maintain a consistent sleep schedule, even on weekends',
            'Turn off all screens at least 1 hour before bed',
            'Ensure your room is cool, dark, and quiet',
            'Try a guided meditation right before sleeping'
        ]
    elif topic == "social":
        tips = [
            'Reach out to one friend or family member today',
            'Join a local club or community class',
            'Limit your time on highly-curated social media',
            'Journal about your feelings to process them'
        ]
    elif topic == "career":
        tips = [
            'Set strict working hours and silence notifications after work',
            'Take your full lunch break away from your desk',
            'Communicate your workload clearly to your manager',
            'Focus on one task at a time rather than multitasking'
        ]
    else:
        tips = [
            'Practice 4-7-8 breathing when feeling overwhelmed',
            'Take a 15-minute walk outside daily',
            'Focus on eating nutritious, balanced meals',
            'Talk to a trusted friend or family member'
        ]

    response = {
        'stress_level': stress_level,
        'message': message,
        'resources': resources,
        'tips': tips
    }
    return jsonify(response)

if __name__ == '__main__':
    # Run server locally (Config item constraint execution)
    app.run(debug=True, port=5000)
