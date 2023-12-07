from sqlalchemy import create_engine
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from models import StudentsCourses
from flask import Flask
from database import db
import numpy as np
from sklearn.metrics import pairwise_distances
# from . import recommendations

engine = create_engine("sqlite:///C:\\Users\\Alape\\Downloads\\data.sqlite3")

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
    print(X_new)

    k = 5  
    # knn = NearestNeighbors(n_neighbors=k, algorithm='auto', metric='euclidean')
    knn = NearestNeighbors(n_neighbors=k, algorithm='auto', metric=non_zero_feature_distance)
    knn.fit(X_scores)

    distances, indices = knn.kneighbors(X_new)

    nearest_neighbor_indices = indices.flatten()
    nearest_neighbor = original_data.iloc[nearest_neighbor_indices]

    nearest_student_ids = nearest_neighbor['student_id'].tolist()

    print("Nearest Neighbor:")
    print(nearest_neighbor)
    print("Corresponding Student IDs:")
    print(nearest_student_ids)
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
    print(unique_courses)

    return unique_courses

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///C:\\Users\\Alape\\Downloads\\data.sqlite3"
db.init_app(app)
app.app_context().push()

nearest_student_ids = get_neighbors(3)
final_courses = queries(nearest_student_ids)


class RecommendationApi():
    def get(self, id):
        nearest_student_ids = get_neighbors(id)
        final_courses = queries(nearest_student_ids)

        return final_courses

# recommendations.add_resource(RecommendationApi, "/api/recommendations")