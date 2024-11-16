from Course import Course
from PySide6.QtCore import QAbstractListModel, Qt
import json
import os

class CurriculumDesigner:
    def __init__(self):
        self.allCourses = []

    @staticmethod
    def GetTestCourses():
        courses = []
        for i in range(0, 10):
            coursePrefix = "ANGD"
            courseNumber = f"{i%4 + 1}{i%3+1}{i%10}{(1+1)%10}"
            courseName = "Dummy"
            courses.append(Course(coursePrefix, int(courseNumber), courseName))

        return courses

    @staticmethod
    def GetAllCourses():
        courses = []
        srcPath = os.path.dirname(os.path.abspath(__file__))
        prjPath = os.path.dirname(srcPath)
        dataPath = os.path.join(prjPath, "data", "data.json")

        with open (dataPath, 'r') as file:
            data = json.load(file)
            for couresInfo in data:
                # "departPrefix":"ANGD",
                # "courseNumber":1001,
                # "courseName":"Orientation to ANGD"
                course = Course(couresInfo["departPrefix"], couresInfo["courseNumber"], couresInfo["courseName"])
                courses.append(course)

        return courses


