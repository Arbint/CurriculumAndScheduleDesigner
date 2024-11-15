class Course:
    def __init__(self, departPrefix = "ANGD", courseNumber = 4399, courseName="ST: Dummy"):
        self.departmentPrefix = departPrefix
        self.courseNumber = courseNumber
        self.courseName = courseName

    def getCredits(self):
        return int(str(self.courseNumber)[1])

    