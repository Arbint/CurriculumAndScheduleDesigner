import os
import json

class Course:
    def __init__(self, departPrefix = "ANGD", courseNumber = 4399, courseName="ST: Dummy"):
        self.departmentPrefix = departPrefix
        self.courseNumber = courseNumber
        self.courseName = courseName

    @staticmethod
    def CreateFromDict(infoDict):
            return Course(infoDict[Course.GetDepartmentPrefixKeyStr()], infoDict[Course.GetCourseNumberKeyStr()], infoDict[Course.GetCourseNameKeyStr()])

    def ToInfoDict(self):
        outDict = {}
        outDict[Course.GetDepartmentPrefixKeyStr()] = self.departmentPrefix
        outDict[Course.GetCourseNumberKeyStr()] = self.courseNumber
        outDict[Course.GetCourseNameKeyStr()] = self.courseName

    @staticmethod
    def GetDepartmentPrefixKeyStr():
        return "departmentPrefix"

    @staticmethod
    def GetCourseNumberKeyStr():
        return "courseNumber"

    @staticmethod
    def GetCourseNameKeyStr():
        return "courseName"

    @staticmethod
    def GetAllCourses():
        courses = []
        srcPath = os.path.dirname(os.path.abspath(__file__))
        prjPath = os.path.dirname(srcPath)
        dataPath = os.path.join(prjPath, "data", "data.json")

        with open (dataPath, 'r') as file:
            data = json.load(file)
            for couresInfo in data:
                course = Course.CreateFromDict(couresInfo)
                courses.append(course)

        return courses

    def GetCredits(self):
        return int(str(self.courseNumber)[1])

    def GetDepartment(self):
        return self.departmentPrefix

    def GetLevel(self):
        return int(str(self.courseNumber)[0])

    def __str__(self):
        return f"{self.departmentPrefix} {self.courseNumber} {self.courseName}"
