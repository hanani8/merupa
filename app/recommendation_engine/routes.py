from sqlalchemy import create_engine
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from app.student.models import StudentsCourses, Student
from app.course.models import Course
from flask import Flask, request
from flask_restful import Resource
from app.database import db
import numpy as np
from sklearn.metrics import pairwise_distances
from app.validation import BusinessValidationError, NotFoundError
from . import recommendations
from app import config


engine = create_engine(config.LocalDevelopmentConfig.SQLALCHEMY_DATABASE_URI)

def non_zero_feature_distance(row_1, X, metric='euclidean'):
    non_zero_indices = np.nonzero(row_1)[0]
    row_1_non_zero = row_1[non_zero_indices]
    X_non_zero = X[non_zero_indices]
    distances = pairwise_distances([row_1_non_zero], X_non_zero.reshape(1, -1), metric=metric)
    return distances.flatten()

def get_neighbors(id):

    view_name = 'student_courses_view'

    query = f"SELECT * FROM {view_name};"
    data = pd.read_sql(query, engine)

    original_data = data

    X_scores = original_data.drop('student_id', axis=1).values


    X_new = data[data["student_id"] == id].values.reshape(1,-1)[:,1:]
    # print(data)
    # print(id)
    # print(X_new)

    k = 5  
    # knn = NearestNeighbors(n_neighbors=k, algorithm='auto', metric='euclidean')
    knn = NearestNeighbors(n_neighbors=k, algorithm='auto', metric=non_zero_feature_distance)
    knn.fit(X_scores)

    distances, indices = knn.kneighbors(X_new)

    nearest_neighbor_indices = indices.flatten()
    nearest_neighbor = original_data.iloc[nearest_neighbor_indices]

    nearest_student_ids = nearest_neighbor['student_id'].tolist()

    # print("Nearest Neighbor:")
    # print(nearest_neighbor)
    # print("Corresponding Student IDs:")
    # print(nearest_student_ids)
    return nearest_student_ids

def queries(nearest_student_ids):

    neighbor_course_list = []

    for nearest_student in nearest_student_ids:
        result_user = (
        db.session.query(StudentsCourses.course_id)
        .filter(StudentsCourses.student_id == nearest_student)
        .filter(StudentsCourses.sequence != 0)
        .order_by(StudentsCourses.sequence)
        .all()
        )

        neighbor_course_list.append(result_user)

    # unique_courses = list(set().union(neighbor_course_list[1], neighbor_course_list[2], neighbor_course_list[3], neighbor_course_list[4]) - set(neighbor_course_list[0]))
    conc_course = neighbor_course_list[1] + neighbor_course_list[2] + neighbor_course_list[3] + neighbor_course_list[4]
    unique_courses = sorted(list(set(conc_course) - set(neighbor_course_list[0])), key=lambda i: conc_course.index(i))
    # print(unique_courses)

    return unique_courses

# nearest_student_ids = get_neighbors(3)
# final_courses = queries(nearest_student_ids)


# Based on a user's course history, output a list of courses that he can do next

def get_next_courses(student_id):
    
    # Get all courses in the system
    courses = Course.query.with_entities(Course.id, Course.level, Course.prerequisites, Course.corequisites).all()

    # Prerequisites
    prerequisites_dict = {}

    for course in courses:
        if course.prerequisites != "None":
            prerequisites_dict[course.id] = list(course.prerequisites.split(", "))
        else:
            prerequisites_dict[course.id] = []

    # Foundational Courses
    foundational_courses = [course for course in courses if course.level == 'FOUNDATIONAL']

    # Diploma Courses
    diploma_courses = [course for course in courses if course.level == 'DIPLOMA']

    # Degree Courses
    degree_courses = [course for course in courses if course.level == 'DEGREE']

    courses = [course.id for course in courses]
    foundational_courses = [course.id for course in foundational_courses]
    diploma_courses = [course.id for course in diploma_courses]
    degree_courses = [course.id for course in degree_courses]


    # Get all courses that a user has done
    student = Student.query.get(student_id)
    done_courses = [student_course.course_id for student_course in student.completed_courses]

    # Remove done_courses from courses
    courses = list(set(courses) - set(done_courses))


    # Check if a student is foundational or diploma
    is_foundational_student = any(course in courses for course in foundational_courses)
    is_diploma_student = any(course in courses for course in diploma_courses)

        
    if is_foundational_student:
        courses = list(set(courses) - set(diploma_courses) - set(degree_courses))
    elif is_diploma_student:
        courses = list(set(courses) - set(degree_courses))

    # Check if any course in the courses list has prerequisites in the courses list
    courses_with_prerequisites = []

    for course in courses:
        for prerequisite in prerequisites_dict[course]:
            if prerequisite in courses:
                courses_with_prerequisites.append(course)
    

    # Remove courses with prerequisites from the courses list
    courses = list(set(courses) - set(courses_with_prerequisites))

    return courses
    
    





class RecommendationApi(Resource):
    def get(self):

        a = request.args.get('roll_no')
        no_of_courses = request.args.get('pref_no', 0)
        mandatory_course = request.args.get('pref_co', "")

        if not no_of_courses.isnumeric():
            return {"error": True,
                    "data": "",
                    "msg": "Number of preferred courses expects numeric input"}

        no_of_courses = int(no_of_courses)

        user_id = (db.session.query(Student.id)
        .filter(Student.rollno == a).first())

        if user_id == None:
            return {"error":True,
                    "data":"",
                    "msg":"Incorrect roll number entered"}

        next_courses = get_next_courses(user_id)

        if mandatory_course != "":
            if mandatory_course not in next_courses:
                return {"error":True,
                        "data":"",
                        "msg":"Incorrect course id entered"}

        if no_of_courses > 4:
            return {"error":True,
                    "data":"",
                    "msg":"Number of preferred courses exceeds limit"}
        


        nearest_student_ids = get_neighbors(user_id)
        total_courses = queries(nearest_student_ids)

        total_courses = [course[0] for course in total_courses]

        final_courses = []
        if mandatory_course in total_courses:
            final_courses.append(mandatory_course) 
            total_courses.remove(mandatory_course)
            no_of_courses -= 1   

        if no_of_courses > len(final_courses):
            final_courses.extend(total_courses[:no_of_courses])

        return final_courses, 200

recommendations.add_resource(RecommendationApi, "/api/recommendations")