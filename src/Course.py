import os
import json

class Course:
    def __init__(self, departPrefix = "ANGD", courseNumber = 4399, courseName="ST: Dummy", finished = False):
        self.departmentPrefix = departPrefix
        self.courseNumber = courseNumber
        self.courseName = courseName
        self.finished = finished

    @staticmethod
    def CreateFromDict(infoDict):
            return Course(infoDict[Course.GetDepartmentPrefixKeyStr()],
                        infoDict[Course.GetCourseNumberKeyStr()],
                        infoDict[Course.GetCourseNameKeyStr()],
                        infoDict[Course.GetCourseFinishedKeyStr()])

    @staticmethod
    def CreateFromDictAllNoFinished(infoDict):
            return Course(infoDict[Course.GetDepartmentPrefixKeyStr()],
                        infoDict[Course.GetCourseNumberKeyStr()],
                        infoDict[Course.GetCourseNameKeyStr()],
                        False)

    def ToInfoDict(self):
        outDict = {}
        outDict[Course.GetDepartmentPrefixKeyStr()] = self.departmentPrefix
        outDict[Course.GetCourseNumberKeyStr()] = self.courseNumber
        outDict[Course.GetCourseNameKeyStr()] = self.courseName
        outDict[Course.GetCourseFinishedKeyStr()] = self.finished
        return outDict

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
    def GetCourseFinishedKeyStr():
        return "finished"

    @staticmethod
    def GetAllCourses():
        courses = []
        srcPath = os.path.dirname(os.path.abspath(__file__))
        prjPath = os.path.dirname(srcPath)
        dataPath = os.path.join(prjPath, "data", "data.json")

        with open (dataPath, 'r') as file:
            data = json.load(file)
            for couresInfo in data:
                course = Course.CreateFromDictAllNoFinished(couresInfo)
                courses.append(course)

        return courses

    def GetCredits(self):
        return int(str(self.courseNumber)[1])

    def GetDepartment(self):
        return self.departmentPrefix

    def GetLevel(self):
        return int(str(self.courseNumber)[0])

    def GetFinished(self):
        return self.finished

    def __str__(self):
        return f"{self.departmentPrefix} {self.courseNumber} {self.courseName}"
