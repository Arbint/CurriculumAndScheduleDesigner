from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QGridLayout, QPushButton, QLabel
from PySide6.QtGui import QAction, QDragEnterEvent, QDragMoveEvent
from PySide6.QtCore import Qt
from CurriculumDesigner import CurriculumDesigner
from CourseWidget import CourseListWidget
from Course import Course


class CourseListGroupWidget(QWidget):
    def __init__(self, title: str):
        super().__init__()
        self.masterLayout = QVBoxLayout() 
        self.setLayout(self.masterLayout)
        listLabel = QLabel(title)
        self.masterLayout.addWidget(listLabel)
        self.listWidget = CourseListWidget()
        self.masterLayout.addWidget(self.listWidget)

    def SetCourses(self, courses: list[Course]):
        self.listWidget.SetCourses(courses)

class CurriculumnDesignerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Curriculumn Designer")
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        
        NewAction = QAction("New", self)
        fileMenu.addAction(NewAction)

        self.centerMasterLayout = QHBoxLayout()
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.centerMasterLayout)
        self.ConfigureSemesterLayout()

        self.ConfigureClassList()

    def ConfigureClassList(self):
        classList = CourseListGroupWidget("classes")
        classList.SetCourses(CurriculumDesigner.GetTestCourses())
        self.centerMasterLayout.addWidget(classList)

    def ConfigureSemesterLayout(self):
        semesterLayout = QGridLayout()
        self.centerMasterLayout.addLayout(semesterLayout)

        freshFall = CourseListGroupWidget("Freshman Fall")
        semesterLayout.addWidget(freshFall, 0, 0)

        freshSpring = CourseListGroupWidget("Freshman Spring")
        semesterLayout.addWidget(freshSpring, 0, 1)

        SophmoreFall = CourseListGroupWidget("Sophmore Fall")
        semesterLayout.addWidget(SophmoreFall, 1, 0)

        SophmoreSpring = CourseListGroupWidget("Sophmore Spring")
        semesterLayout.addWidget(SophmoreSpring, 1, 1)

        JuniorFall = CourseListGroupWidget("Junior Fall")
        semesterLayout.addWidget(JuniorFall, 2, 0)

        JuniorSpring = CourseListGroupWidget("Junior Spring")
        semesterLayout.addWidget(JuniorSpring, 2, 1)

        SeniorFall = CourseListGroupWidget("Senior Fall")
        semesterLayout.addWidget(SeniorFall, 3, 0)

        SeniorSpring = CourseListGroupWidget("Senior Spring")
        semesterLayout.addWidget(SeniorSpring, 3, 1)

if __name__ == "__main__":
    app = QApplication()
    window = CurriculumnDesignerWindow()
    window.show()
    app.exec()