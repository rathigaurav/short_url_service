import json
import requests

# the Docker container is running on localhost:8000

def test_create_short_url():
    # Test creating a short URL
    input_data = {
        "long_url" : 'https://www.cloudflare.com', # should be valid http/https/ftp URL
        "expiration_time": 2212729328000  # should be int
    }
    response = requests.post("http://localhost:8000/short_url/create", json=input_data)
    assert response.status_code == 201
    assert "short_url" in response.json()
    short_url = response.json().get('short_url')
    requests.delete(f"http://localhost:8000/short_url/delete/{short_url}")

def test_create_short_url_no_long_url_is_passed():
    input_data = {}
    response = requests.post("http://localhost:8000/short_url/create", json=input_data)
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'long_url'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_create_short_url_invalid_long_url_is_passed():
    input_data = {
        "long_url" : 'www.cloudflare.com',
        "expiration_time": 2212729328000  
    }
    response = requests.post("http://localhost:8000/short_url/create", json=input_data)
    assert response.status_code == 400
    assert response.json() == {'detail': {'error': "Provide a valid URL starting with 'http' or 'https' or 'ftp'. Ex:https://www.cloudflare.com/"}}

def test_create_short_url_invalid_expiration_time_is_passed():
    input_data = {
        "long_url" : 'https://www.cloudflare.com',
        "expiration_time": 212729328000  
    }
    response = requests.post("http://localhost:8000/short_url/create", json=input_data)
    assert response.status_code == 400
    assert response.json() == {'detail': {'error': 'Expiration time must be a future timestamp(integer) in milliseconds. Ex:1707807728000'}}

def test_delete_short_url():
    input_data = {
        "long_url" : 'https://www.cloudflare.com',
        "expiration_time": 2212729328000  
    }
    response = requests.post("http://localhost:8000/short_url/create", json=input_data)
    short_url = response.json().get('short_url')
    assert response.status_code == 201
    # Test deleting a short URL
    response = requests.delete(f"http://localhost:8000/short_url/delete/{short_url}")
    assert response.status_code == 200
    assert response.json()["message"] == "Short URL successfully deleted."

def test_get_long_url():
    input_data = {
        "long_url" : 'https://www.cloudflare.com',
        "expiration_time": 2212729328000  # should be int
    }
    response = requests.post("http://localhost:8000/short_url/create", json=input_data)
    short_url = response.json().get('short_url')
    assert response.status_code == 201
    # Test get a long URL
    response = requests.get(f"http://localhost:8000/short_url/lookup/{short_url}")
    assert response.status_code == 200
    requests.delete(f"http://localhost:8000/short_url/delete/{short_url}")
