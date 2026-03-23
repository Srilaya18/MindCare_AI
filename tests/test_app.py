import json
import pytest
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """GET / should return 200 and contain MindCare."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'MindCare' in response.data


def test_analyze_missing_text(client):
    """POST /analyze with empty text should return 400."""
    response = client.post(
        '/analyze',
        data=json.dumps({'text': ''}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


def test_analyze_text_too_long(client):
    """POST /analyze with text > 1000 chars should return 400."""
    response = client.post(
        '/analyze',
        data=json.dumps({'text': 'x' * 1001}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data


@patch('app.classify_and_respond')
def test_analyze_success(mock_classify, client):
    """POST /analyze with valid text should return 200 with stress data."""
    mock_classify.return_value = {
        "stress_level": "HIGH",
        "empathy": "I hear you, and I'm here for you.",
        "tips": ["Take a deep breath", "Talk to someone you trust"],
        "helplines": [{"name": "iCall", "number": "9152987821"}]
    }

    response = client.post(
        '/analyze',
        data=json.dumps({'text': 'I feel overwhelmed and cannot cope'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['stress_level'] == 'HIGH'
    assert 'empathy' in data
    assert isinstance(data['tips'], list)
    assert isinstance(data['helplines'], list)


@patch('app.classify_and_respond')
def test_analyze_low_stress(mock_classify, client):
    """Should handle LOW stress correctly."""
    mock_classify.return_value = {
        "stress_level": "LOW",
        "empathy": "Sounds like you're doing okay!",
        "tips": ["Keep up the good work"],
        "helplines": []
    }

    response = client.post(
        '/analyze',
        data=json.dumps({'text': 'Everything is going fine today'}),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['stress_level'] == 'LOW'


@patch('app.classify_and_respond')
def test_analyze_openai_error(mock_classify, client):
    """Should return 500 if OpenAI call fails."""
    mock_classify.side_effect = Exception("OpenAI API error")

    response = client.post(
        '/analyze',
        data=json.dumps({'text': 'I am feeling stressed'}),
        content_type='application/json'
    )
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data
