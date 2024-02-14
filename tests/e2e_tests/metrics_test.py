import json
import requests

def test_get_metrics():
    # Test creating a short URL
    input_data = {
        "long_url" : 'https://www.cloudflare.com', # should be valid http/https/ftp URL
        "expiration_time": 2212729328000  # should be int
    }
    response = requests.post("http://localhost:8000/short_url/create", json=input_data)
    assert response.status_code == 201
    short_url = response.json().get('short_url')
    get_long_url = f"http://localhost:8000/short_url/lookup/{short_url}"
    requests.get(get_long_url)
    requests.get(get_long_url)
    requests.get(get_long_url)
    get_metrics_endpoint = f"http://localhost:8000/metrics/access_count/{short_url}"
    response = requests.get(get_metrics_endpoint)
    assert response.status_code == 200
    response = requests.delete(f"http://localhost:8000/short_url/delete/{short_url}")
    assert response.status_code == 200

def test_get_metrics_for_invalid_url():
    get_metrics_endpoint = f"http://localhost:8000/metrics/access_count/https://shorty/test123"
    response = requests.get(get_metrics_endpoint)
    assert response.status_code == 404
    assert response.json() == { 'detail': { "error": "short_url: https://shorty/test123 not found." } }