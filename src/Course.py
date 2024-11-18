import os
import json

class Course:
    def __init__(self, departPrefix = "ANGD", courseNumber = 4399, courseName="ST: Dummy", finished = False, note = ""):
        self.departmentPrefix = departPrefix
        self.courseNumber = courseNumber
        self.courseName = courseName
        self.finished = finished
        self.note = note 

    def GetCredits(self):
        return int(str(self.courseNumber)[1])

    def GetDepartment(self):
        return self.departmentPrefix

    def GetLevel(self):
        return int(str(self.courseNumber)[0])

    def GetFinished(self):
        return self.finished

    def __str__(self):
        baseInfo = f"{self.departmentPrefix} {self.courseNumber} {self.courseName}"
        if self.note != "":
            baseInfo += f"\n({self.note})\n"
        
        return baseInfo

    @staticmethod
    def CreateFromDict(infoDict):
            return Course(infoDict[Course.GetDepartmentPrefixKeyStr()],
                        infoDict[Course.GetCourseNumberKeyStr()],
                        infoDict[Course.GetCourseNameKeyStr()],
                        Course.GetBool(infoDict, Course.GetCourseFinishedKeyStr()),
                        Course.GetStr(infoDict, Course.GetCourseNoteKeyStr())
                        )


    @staticmethod
    def GetOrNone(infoDict, keyStr):
        if keyStr in infoDict:
            return infoDict[keyStr]

        return None

    @staticmethod
    def GetStr(infoDict, keyStr)->str:
        foundVal = Course.GetOrNone(infoDict, keyStr)
        return foundVal if foundVal else ""

    @staticmethod
    def GetBool(infoDict, keyStr)->bool:
        foundVal = Course.GetOrNone(infoDict, keyStr)
        return foundVal if foundVal else False

    def ToInfoDict(self):
        outDict = {}
        outDict[Course.GetDepartmentPrefixKeyStr()] = self.departmentPrefix
        outDict[Course.GetCourseNumberKeyStr()] = self.courseNumber
        outDict[Course.GetCourseNameKeyStr()] = self.courseName
        outDict[Course.GetCourseFinishedKeyStr()] = self.finished
        outDict[Course.GetCourseNoteKeyStr()] = self.note
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
    def GetCourseNoteKeyStr():
        return "note"

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