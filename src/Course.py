class Course:
    def __init__(self, departPrefix = "ANGD", courseNumber = 4399, courseName="ST: Dummy"):
        self.departmentPrefix = departPrefix
        self.courseNumber = courseNumber
        self.courseName = courseName

    def GetCredits(self):
        return int(str(self.courseNumber)[1])

    def GetDepartment(self):
        return self.departmentPrefix

    def GetLevel(self):
        return int(str(self.courseNumber)[0])

    def __str__(self):
        return f"{self.departmentPrefix} {self.courseNumber} {self.courseName}"