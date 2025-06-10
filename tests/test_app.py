import os
import sys
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from immigration_navigator.backend import app as fastapi_app

client = TestClient(fastapi_app)

def test_root():
    r = client.get('/')
    assert r.status_code == 200

def test_immigration():
    data = {
        "nationality": "Canada",
        "current_visa": "F1",
        "target_visa": "H1B",
        "occupation": "Engineer"
    }
    r = client.post('/api/immigration', json=data)
    assert r.status_code == 200
    assert 'forms' in r.json()

def test_wellness():
    r = client.post('/api/wellness', json={'message': 'I am sad'})
    assert r.status_code == 200
    assert 'advice' in r.json()
