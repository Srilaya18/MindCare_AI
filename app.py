import os
import json
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are MindCare AI, a compassionate mental health support assistant.
Analyze the user's message and respond ONLY with a valid JSON object (no markdown, no extra text) in this exact format:
{
  "stress_level": "HIGH" or "MEDIUM" or "LOW",
  "empathy": "A warm, 2-3 sentence empathetic response acknowledging feelings",
  "tips": ["tip 1", "tip 2", "tip 3", "tip 4"],
  "helplines": [
    {"name": "iCall (India)", "number": "9152987821"},
    {"name": "Vandrevala Foundation", "number": "1860-2662-345"},
    {"name": "NIMHANS", "number": "080-46110007"}
  ]
}

Stress classification rules:
- HIGH: mentions crisis, hopeless, suicidal, overwhelming, panic, can't cope, breakdown
- MEDIUM: mentions stressed, anxious, worried, sad, struggling, exhausted, pressure
- LOW: mild sadness, general concern, seeking advice, feeling slightly off

Always respond with ONLY the JSON object. No preamble, no explanation outside JSON.
"""


def classify_and_respond(user_text):
    """Send user text to OpenAI and return parsed response."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0.7,
        max_tokens=600
    )
    raw = response.choices[0].message.content.strip()
    return json.loads(raw)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    user_text = data.get("text", "").strip()

    if not user_text:
        return jsonify({"error": "No text provided"}), 400

    if len(user_text) > 1000:
        return jsonify({"error": "Text too long. Please keep it under 1000 characters."}), 400

    try:
        result = classify_and_respond(user_text)
        return jsonify(result)
    except json.JSONDecodeError:
        return jsonify({"error": "AI response parsing failed. Please try again."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1", host="0.0.0.0", port=5000)
