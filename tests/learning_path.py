import requests

base_url = "http://localhost:5000"

def test_learning_path_correct_id_1():
    endpoint = base_url + "/api/learningpath/1"
    response = requests.get(endpoint)
    data = response.json()
    assert response.status_code == 200
    assert data['error'] == False
    assert data['msg'] == "learning path returned"
    assert data['data']['id'] == 1


def test_learning_path_correct_id_2():
    endpoint = base_url + "/api/learningpath/2"
    response = requests.get(endpoint)
    data = response.json()
    assert response.status_code == 200
    assert data['error'] == False
    assert data['msg'] == "learning path returned"
    assert data['data']['id'] == 2


def test_learning_path_wrong_id_465():
    endpoint = base_url + "/api/learningpath/465"
    response = requests.get(endpoint)
    data = response.json()
    assert response.status_code == 404
    assert data['error'] == True
    assert data['msg'] == "No such learning path found"
    assert data['data'] == ""

def test_learning_path_wrong_id_470():
    endpoint = base_url + "/api/learningpath/470"
    response = requests.get(endpoint)
    data = response.json()
    assert response.status_code == 404
    assert data['error'] == True
    assert data['msg'] == "No such learning path found"
    assert data['data'] == ""

def test_learning_path_upvote_2():
    endpoint = base_url + "/api/learningpath/upvote/2"
    response = requests.patch(endpoint)
    data = response.json()
    assert response.status_code == 200
    assert data['error'] == False
    assert data['msg'] == "Learning path successfully upvoted"
    assert data['data'] == ""

def test_learning_path_upvote_3():
    endpoint = base_url + "/api/learningpath/upvote/3"
    response = requests.patch(endpoint)
    data = response.json()
    assert response.status_code == 200
    assert data['error'] == False
    assert data['msg'] == "Learning path successfully upvoted"
    assert data['data'] == ""

def test_learning_path_already_upvoted_2():
    endpoint = base_url + "/api/learningpath/upvote/2"
    response = requests.patch(endpoint)
    data = response.json()
    assert response.status_code == 400
    assert data['error'] == True
    assert data['msg'] == "Already upvoted"
    assert data['data'] == ""

def test_learning_path_already_upvoted_3():
    endpoint = base_url + "/api/learningpath/upvote/3"
    response = requests.patch(endpoint)
    data = response.json()
    assert response.status_code == 400
    assert data['error'] == True
    assert data['msg'] == "Already upvoted"
    assert data['data'] == ""