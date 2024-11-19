from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIntValidator
from Course import Course

class ConfigureCourseWidget(QWidget):
    onAddCourse = Signal(str, int, str) 

    @classmethod
    def ConfigureMode():
        return 0

    @classmethod
    def AddMode():
        return 1

    def __init__(self, parent = None, mode = 0, course: Course = None):
        super().__init__(parent)
        self.setMinimumSize(400, 200)
        self.setWindowFlags(Qt.WindowType.Window)
        self.show()
        addCourseLayout = QGridLayout()
        self.setLayout(addCourseLayout)
        courseDepartmentLabel = QLabel("Couse Department Label:") 
        self.courseDepartmentLineEdit = QLineEdit("ANGD")
        courseNumberLabel = QLabel("Couse Number")
        self.courseNumberLineEdit = QLineEdit()
        self.courseNumberLineEdit.setValidator(QIntValidator())
        courseNameLabel=QLabel("CourseName")
        self.courseNameLineEdit=QLineEdit()


        addCourseLayout.addWidget(courseDepartmentLabel, 0, 0)
        addCourseLayout.addWidget(self.courseDepartmentLineEdit, 0, 1)

        addCourseLayout.addWidget(courseNumberLabel, 1, 0)
        addCourseLayout.addWidget(self.courseNumberLineEdit, 1, 1)

        addCourseLayout.addWidget(courseNameLabel, 2, 0)
        addCourseLayout.addWidget(self.courseNameLineEdit, 2, 1)

        if mode == ConfigureCourseWidget.AddMode(): 
            addCourseBtn = QPushButton("Add Course")
            addCourseLayout.addWidget(addCourseBtn)
            addCourseBtn.clicked.connect(self.AddCourseBtnClicked)

        elif mode == ConfigureCourseWidget.ConfigureMode():
            configureBtn = QPushButton("Confirm Course")
            addCourseLayout.addWidget(configureBtn)
            configureBtn.clicked.connect(self.ConfigureCourseBtnClicked)

        cancelBtn = QPushButton("Cancel")
        addCourseLayout.addWidget(cancelBtn)
        cancelBtn.clicked.connect(lambda : self.close())

    def ConfigureCourseBtnClicked(self):
        print(f"configuring")

    def AddCourseBtnClicked(self):
        courseDepartmentPrefix = self.courseDepartmentLineEdit.text() 
        courseNumber = int(self.courseNumberLineEdit.text())
        courseName = self.courseNameLineEdit.text()

        self.onAddCourse.emit(courseDepartmentPrefix, courseNumber, courseName)
        self.close()