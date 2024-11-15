from Course import Course

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

    