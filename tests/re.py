import requests

base_url = "http://localhost:5000"

def test_re_more_than_4_courses():
    endpoint = base_url + "/api/recommendations?roll_no=&pref_no=5&pref_co="
    response = requests.get(endpoint)
    data = response.json()
    # assert response.status_code == 200
    assert data['error'] == True
    assert data['msg'] == "Number of preferred courses exceeds limit"
    assert data['data'] == ""

def test_re_wrong_roll_no():
    endpoint = base_url + "/api/recommendations?roll_no=12345&pref_no=&pref_co="
    response = requests.get(endpoint)
    data = response.json()
    # assert response.status_code == 200
    assert data['error'] == True
    assert data['msg'] == "Incorrect roll number entered"
    assert data['data'] == ""


def test_re_correct_roll_no_course_no_3():
    endpoint = base_url + "/api/recommendations?roll_no=23f1000076&pref_no=3&pref_co="
    response = requests.get(endpoint)
    data = response.json()
    # assert response.status_code == 200
    # assert data['error'] == False
    # assert data['msg'] == "Recommended courses returned"
    assert data[0] == "CS2001"

def test_re_correct_roll_no():
    endpoint = base_url + "/api/recommendations?roll_no=21f2000201&pref_no=3&pref_co="
    response = requests.get(endpoint)
    data = response.json()
    assert response.status_code == 200
    assert data[0] == "MA1004"