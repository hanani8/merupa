import requests

base_url = "http://localhost:5000"

def test_course_correct_id():
    endpoint = base_url + "/api/course/course/MA1001"
    response = requests.get(endpoint)
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == "MA1001"