import requests

base_url = "http://localhost:5000"

def test_course_correct_id():
    endpoint = base_url + "/api/course/MA1001"
    response = requests.get(endpoint)
    data = response.json()
    assert response.status_code == 200
    assert data['id'] == "MA1001"

def test_course_incorrect_id():
    endpoint = base_url + "/api/course/ABC1001"
    response = requests.get(endpoint)
    data = response.json()
    assert response.status_code == 400
    assert data["error_code"] == "C001"
    assert data["error_message"] == "Course Not Found"

def test_course_rating_incorrect_rating_type():
    endpoint = base_url + "/api/course/MA1001/rating"
    response = requests.post(endpoint, json={"rating_type":"Custom Rating", "rating_value":7.5, "student_id": 3})
    data = response.json()
    assert response.status_code == 400
    assert data["error_code"] == "R001"
    assert data["error_message"] == "Rating Type Not Found"

def test_course_rating_incorrect_course_id():
    endpoint = base_url + "/api/course/ABC3001/rating"
    response = requests.post(endpoint, json={"rating_type":"Assignments", "rating_value":7.5, "student_id": 3})
    data = response.json()
    assert response.status_code == 400
    assert data["error_code"] == "C001"
    assert data["error_message"] == "Course Not Found"

def test_course_rating_incorrect_student_id():
    endpoint = base_url + "/api/course/MA1001/rating"
    response = requests.post(endpoint, json={"rating_type":"Assignments", "rating_value":7.5, "student_id": 300})
    data = response.json()
    assert response.status_code == 400
    assert data["error_code"] == "S001"
    assert data["error_message"] == "Student Not Found"

def test_course_successful_rating():
    endpoint = base_url + "/api/course/MA1001/rating"
    response = requests.post(endpoint, json={"rating_type":"Course Support", "rating_value":7.5, "student_id": 3})
    data = response.json()
    assert response.status_code == 201

def test_course_no_previous_feedback():
    endpoint = base_url + "/api/course/CS2004/feedback"
    response = requests.put(endpoint, json={"feedback": "GREAT", "student_id":3})
    data = response.json()
    # assert response.status_code == 200
    assert data["error_code"] == "CF003"
    assert data["error_message"] == "No Previous Feedback to Update"

# def test_course_successful_downvote():
#     endpoint = base_url + "/api/course/CS2004/feedback/vote"
#     response = requests.put(endpoint, json={"vote": "downvote", "student_id": 3})
#     data = response.json()
#     print(data)
#     assert response.status_code == 200
#     assert data["error_code"] == "CF003"
#     assert data["error_message"] == "No Previous Feedback to Update"

# def test_course_delete_feedback():
#     endpoint = base_url + "/api/course/CS2004/feedback"
#     response = requests.delete(endpoint, {"student_id": 3})
#     data = response.json()
#     assert response.status_code == 200
#     assert data == "Successfully Deleted"