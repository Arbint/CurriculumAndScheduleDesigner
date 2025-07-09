from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel, QPushButton, QCheckBox, QTextEdit
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIntValidator
from degreeplaner.Course import Course

class CourseConfigureWidget(QWidget):
    onAddCourse = Signal(str, int, str, bool, str) 
    onConfigureCourse = Signal()

    @staticmethod
    def ConfigureMode():
        return 0

    @staticmethod
    def AddMode():
        return 1

    def __init__(self, parent = None, mode = 0, course: Course = None):
        super().__init__(parent)
        self.setMinimumSize(400, 200)
        self.setWindowFlags(Qt.WindowType.Window)
        self.show()
        configureCourseLayout = QGridLayout()
        self.setLayout(configureCourseLayout)

        courseDepartmentLabel = QLabel("Couse Department Label:") 
        self.courseDepartmentLineEdit = QLineEdit("ANGD")
        
        courseNumberLabel = QLabel("Couse Number:")
        self.courseNumberLineEdit = QLineEdit()
        self.courseNumberLineEdit.setValidator(QIntValidator())

        courseNameLabel=QLabel("Course Name:")
        self.courseNameLineEdit=QLineEdit()

        courseFinishedLabel=QLabel("Finished:")
        self.courseFinishedCheckbox=QCheckBox()

        courseNoteLabel=QLabel("Note:")
        self.couresNoteTextEdit= QTextEdit()

        configureCourseLayout.addWidget(courseDepartmentLabel, 0, 0)
        configureCourseLayout.addWidget(self.courseDepartmentLineEdit, 0, 1)

        configureCourseLayout.addWidget(courseNumberLabel, 1, 0)
        configureCourseLayout.addWidget(self.courseNumberLineEdit, 1, 1)

        configureCourseLayout.addWidget(courseNameLabel, 2, 0)
        configureCourseLayout.addWidget(self.courseNameLineEdit, 2, 1)

        configureCourseLayout.addWidget(courseFinishedLabel, 3, 0)
        configureCourseLayout.addWidget(self.courseFinishedCheckbox, 3, 1)

        configureCourseLayout.addWidget(courseNoteLabel, 4, 0)
        configureCourseLayout.addWidget(self.couresNoteTextEdit, 4, 1)

        if mode == CourseConfigureWidget.AddMode(): 
            addCourseBtn = QPushButton("Add Course")
            configureCourseLayout.addWidget(addCourseBtn)
            addCourseBtn.clicked.connect(self.AddCourseBtnClicked)

        elif mode == CourseConfigureWidget.ConfigureMode():
            self.LoadCourseInfo(course)
            configureBtn = QPushButton("Confirm Change")
            configureCourseLayout.addWidget(configureBtn)
            configureBtn.clicked.connect(lambda : self.ConfigureCourseBtnClicked(course))

        cancelBtn = QPushButton("Cancel")
        configureCourseLayout.addWidget(cancelBtn)
        cancelBtn.clicked.connect(lambda : self.close())

    def LoadCourseInfo(self, courseInfoSrc : Course):
        self.courseDepartmentLineEdit.setText(courseInfoSrc.departmentPrefix) 
        self.courseNumberLineEdit.setText(str(courseInfoSrc.courseNumber))
        self.courseNameLineEdit.setText(courseInfoSrc.courseName)
        self.courseFinishedCheckbox.setChecked(courseInfoSrc.finished)
        self.couresNoteTextEdit.setText(courseInfoSrc.note)

    def ConfigureCourseBtnClicked(self, courseToConfiture: Course):
        courseToConfiture.UpdateData(*self.GetCourseConfigFromWidgets())
        self.onConfigureCourse.emit()
        self.close()

    def GetCourseConfigFromWidgets(self):
        courseDepartmentPrefix = self.courseDepartmentLineEdit.text() 
        courseNumber = int(self.courseNumberLineEdit.text())
        courseName = self.courseNameLineEdit.text()
        courseFinished = self.courseFinishedCheckbox.isChecked()
        courseNote = self.couresNoteTextEdit.toPlainText()
        return courseDepartmentPrefix, courseNumber, courseName, courseFinished, courseNote


    def AddCourseBtnClicked(self):
        self.onAddCourse.emit(*self.GetCourseConfigFromWidgets())
        self.close()