from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QGridLayout
from CourseListWidget import CourseListViewGroup
from CourseList import CourseListModel
from Course import Course

class CurriculumnPlaner(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setCentralWidget(QWidget())
        self.centralMasterLayout = QHBoxLayout()
        self.centralWidget().setLayout(self.centralMasterLayout)

        self.setWindowTitle("Curriculum Planer")
        self.ConfigureAllClassList()
        self.ConfigureSemesters()
        self.ConfigureFinishedClassList()
        
    def ConfigureAllClassList(self):
        self.allClassListViewGrp = CourseListViewGroup()
        self.allClassModel = CourseListModel(Course.GetAllCourses(), "All Classes")
        self.allClassListViewGrp.BindModel(self.allClassModel)
        self.centralMasterLayout.addWidget(self.allClassListViewGrp)

    def ConfigureFinishedClassList(self):
        self.finishedClassListViewGrp = CourseListViewGroup()
        self.finishedClassModel = CourseListModel([], "Finshed Classes")
        self.finishedClassListViewGrp.BindModel(self.finishedClassModel)
        self.centralMasterLayout.addWidget(self.finishedClassListViewGrp)

    def AddSemester(self, name: str, parentGrid: QGridLayout, x, y, semesterCourses : list[Course] = None):
        semesterView = CourseListViewGroup()
        semesterModel = CourseListModel(semesterCourses, name)
        semesterView.BindModel(semesterModel)
        parentGrid.addWidget(semesterView, x, y)
        self.semestersModels[name] = semesterModel

    def ConfigureSemesters(self):
        self.semestersModels = {}
        semesterLayout = QGridLayout()
        self.centralMasterLayout.addLayout(semesterLayout)

        self.AddSemester("Freshman Fall", semesterLayout, 0, 0)
        self.AddSemester("Freshman Spring", semesterLayout, 0, 1)
        self.AddSemester("Freshman Summer", semesterLayout, 0, 2)

        self.AddSemester("Sophmore Fall", semesterLayout, 1, 0)
        self.AddSemester("Sophmore Spring", semesterLayout, 1, 1)
        self.AddSemester("Sophmore Summer", semesterLayout, 1, 2)

        self.AddSemester("Junior Fall", semesterLayout, 2, 0)
        self.AddSemester("Junior Spring", semesterLayout, 2, 1)
        self.AddSemester("Junior Summer", semesterLayout, 2, 2)

        self.AddSemester("Senior Fall", semesterLayout, 3, 0)
        self.AddSemester("Senior Spring", semesterLayout, 3, 1)


if __name__ == "__main__":
    app = QApplication()
    planer = CurriculumnPlaner()
    planer.show()
    app.exec()

