import requests

def test_api_health():
    response = requests.get("http://api:8000/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_api_inference():
    response = requests.post("http://api:8000/inference", json={"input": "test"})
    assert response.status_code == 200
    assert "output" in response.json()