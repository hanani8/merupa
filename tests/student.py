import requests

base_url = "http://localhost:5000"
from app import init_app
app = init_app()
from app.student.models import Student



def test_student_correct_id():
    endpoint = base_url + "/api/student/2"
    response = requests.get(endpoint)
    data = response.json()
    assert response.status_code == 200
    assert data["error"] == False
    assert data["msg"] == "Fetched student successfully"
    assert data["data"]["id"] == 2

def test_student_incorrect_id():
    endpoint = base_url + "/api/student/1000"
    response = requests.get(endpoint)
    data = response.json()
    assert response.status_code == 404
    assert data["error"] == True
    assert data["msg"] == "Student Not found"
    assert data["data"]["id"] == 0

def test_student_missing_field_at_creation_1():
    endpoint = base_url + "/api/admin/student"
    response = requests.post(endpoint, json={"name": "21f1001235", "password": "21f1001235", "phone": 9012345678}, headers={"Content-Type": "application/json"})
    data = response.json()
    assert response.status_code == 400
    print(data)
    assert data["error"] == True
    assert data["msg"] == "One or more fields are empty"
    assert data["data"]["id"] == 0

def test_student_missing_field_at_creation_2():
    endpoint = base_url + "/api/admin/student"
    response = requests.post(endpoint, json={"name": "21f1001235", "phone": 9012345678})
    data = response.json()
    assert response.status_code == 400
    assert data["error"] == True
    assert data["msg"] == "One or more fields are empty"
    assert data["data"]["id"] == 0

def test_student_duplicate_email():
    endpoint = base_url + "/api/admin/student"
    response = requests.post(endpoint, json = {"email": "21f1001346@ds.study.iitm.ac.in", "name": "21f1001235", "password": "21f1001235", "phone": 9012345678})
    print(response.text)
    data = response.json()
    assert response.status_code == 400
    assert data["error"] == True
    assert data["msg"] == "Email already exists"
    assert data["data"]["id"] == 0

def test_student_correct_data_for_creation():
    endpoint = base_url + "/api/admin/student"
    response = requests.post(endpoint, json={"email": "21f1001235@ds.study.iitm.ac.in", "name": "21f1001235", "password": "21f1001235", "phone": 9012345678})
    data = response.json()
    assert response.status_code == 201
    assert data["error"] == False
    assert data["msg"] == "Student created successfully"

def test_student_suscessful_deletion():
    with app.app_context():
        students = Student.query.all()
        student_id  = students[len(students) - 1].id
        endpoint = base_url + "/api/admin/student/" + str(student_id)
        response = requests.delete(endpoint)
        data = response.json()
        assert response.status_code == 200
        assert data["error"] == False
        assert data["msg"] == "Student deleted successfully"
        assert data["data"] == ""

def test_student_unsuscessful_deletion():
    endpoint = base_url + "/api/admin/student/1000"
    response = requests.delete(endpoint)
    data = response.json()
    assert response.status_code == 404
    assert data["error"] == True
    assert data["msg"] == "Student not found"
    assert data["data"] == ""

def test_student_suscessful_edit():
    endpoint = base_url + "/api/admin/student/32"
    response = requests.put(endpoint, json={"email": "21f1001237@ds.study.iitm.ac.in", "name": "21f1001234", "phone": 9012345678})
    data = response.json()
    assert response.status_code == 200
    assert data["error"] == False
    assert data["msg"] == "Student edited successfully"
    assert data["data"]["id"] == 32

def test_student_suscessful_score_edit():
    endpoint = base_url + "/api/admin/student/33"
    response = requests.patch(endpoint, json={"course_id": "HS1001", "score": 95, "sequence": 1})
    data = response.json()
    assert response.status_code == 200
    assert data["error"] == False
    assert data["msg"] == "Student scores updated successfully"