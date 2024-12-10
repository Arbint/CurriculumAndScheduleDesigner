from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QLabel, QLineEdit, QPushButton, QSplitter
from PySide6.QtGui import QAction, QIntValidator
from PySide6.QtCore import Qt, Signal
from CourseListWidget import CourseListViewGroup
from CourseConfigureWidget import CourseConfigureWidget
from CourseList import CourseListModel
from Course import Course
from SearchCourseWidget import SearchCourseWidget
import os
import SaveUtilties

class CurriculumnPlaner(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ConfigureMainMenu()
        self.setCentralWidget(QWidget())
        self.centralMasterLayout = QHBoxLayout()
        self.centralWidget().setLayout(self.centralMasterLayout)

        self.mainSpliter = QSplitter()
        self.centralMasterLayout.addWidget(self.mainSpliter)

        self.setWindowTitle("Curriculum Planer")
        self.models = {}
        self.ConfigureAllClassList()
        self.ConfigureSemesters()
        self.ConfigureFinishedClassList()
        
    def ConfigureMainMenu(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("File")
        
        saveAction = QAction("Save", self)
        saveAction.triggered.connect(self.SaveFile)
        fileMenu.addAction(saveAction)

        loadAction = QAction("Load", self)
        loadAction.triggered.connect(self.LoadFile)
        fileMenu.addAction(loadAction)

        addCourseAction = QAction("Add Course", self)
        addCourseAction.triggered.connect(self.AddCourse)
        fileMenu.addAction(addCourseAction)

        searchCourseAction = QAction("Serach Course", self)
        searchCourseAction.triggered.connect(self.SearchCoure)
        fileMenu.addAction(searchCourseAction)

    def SearchCoure(self):
        searchWidget = SearchCourseWidget(self)
        searchWidget.startSearch.connect(self.FindAndSelectionCourseWithKeyword)

    def FindAndSelectionCourseWithKeyword(self, keyword):
        for model in self.models.values():
            model.SelectWithKeyword(keyword)

    def AddCourse(self):
        addCourseWidget = CourseConfigureWidget(self, CourseConfigureWidget.AddMode())
        addCourseWidget.onAddCourse.connect(self.allClassModel.AddNewCourse)

    def DuplicateCourse(self, courseToDuplicate: Course):
        self.courses.append(courseToDuplicate.MakeDuplicate())
        self.layoutChanged.emit()

    def SaveFile(self):
        savePath, selectedFilter = QFileDialog().getSaveFileName(self, "Save File", self.GetDefaultSaveDir(), self.GetSaveFileFilters())
        SaveUtilties.SaveModelsToJson(self.models.values(), savePath)

    def GetDefaultSaveDir(self):
        srcDir = os.path.dirname(__file__)
        prjDir = os.path.dirname(srcDir)
        saveDir = os.path.join(prjDir, "saves")
        return saveDir


    def LoadFile(self):
        loadPath, _ = QFileDialog().getOpenFileName(self, "Load File", self.GetDefaultSaveDir(), self.GetSaveFileFilters())
        loadedModelDict = SaveUtilties.LoadJsonDictFromPath(loadPath)
        for loadedModelName, courseList in loadedModelDict.items():
            foundModel = self.models[loadedModelName]
            foundModel.Clear()
            foundModel.InitCoursesFromList(courseList)

    def GetSaveFileFilters(self):
        filters = ""
        filters += "Json Files (*.json)"
        return filters

    def ConfigureAllClassList(self):
        self.allClassListViewGrp = CourseListViewGroup()
        self.allClassModel = CourseListModel(Course.GetAllCourses(), self.GetAllClassesNameStr())
        self.allClassListViewGrp.BindModel(self.allClassModel)
        self.mainSpliter.addWidget(self.allClassListViewGrp)
        self.models[self.GetAllClassesNameStr()] = self.allClassModel

    def ConfigureFinishedClassList(self):
        self.finishedClassListGrp = CourseListViewGroup()
        self.finishedClassListModel = CourseListModel([], self.GetFinishedClassesNameStr())
        self.finishedClassListGrp.BindModel(self.finishedClassListModel)
        self.mainSpliter.addWidget(self.finishedClassListGrp)
        self.models[self.GetFinishedClassesNameStr()] = self.finishedClassListModel       
        self.finishedClassListModel.layoutChanged.connect(self.UpdateTotoalCredits)

    def AddSemester(self, name: str, parentGrid: QGridLayout, x, y, semesterCourses : list[Course] = None):
        semesterView = CourseListViewGroup()
        semesterModel = CourseListModel(semesterCourses, name)
        semesterView.BindModel(semesterModel)
        parentGrid.addWidget(semesterView, x, y)
        self.semestersModels[name] = semesterModel
        self.models[name] = semesterModel

    def ConfigureSemesters(self):
        self.semestersModels = {}
        semesterWidget = QWidget()
        semesterLayout = QGridLayout(parent=semesterWidget)
        self.mainSpliter.addWidget(semesterWidget)

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

        self.totalCreditLabel = QLabel("")
        semesterLayout.addWidget(self.totalCreditLabel, 3, 2)

        for semesterModel in self.semestersModels.values():
            semesterModel: CourseListModel = semesterModel
            semesterModel.layoutChanged.connect(self.UpdateTotoalCredits)
        
    def UpdateTotoalCredits(self):
        credits = 0
        for semesterModel in self.semestersModels.values():
            semesterModel: CourseListModel = semesterModel
            credits += semesterModel.GetTotalCredits()
        credits += self.finishedClassListModel.GetTotalCredits()
        self.totalCreditLabel.setText(f"total credits: {credits}")

    def GetAllClassesNameStr(self):
        return "All Classes"

    def GetFinishedClassesNameStr(self):
        return "Finished Classes"

if __name__ == "__main__":
    app = QApplication()
    planer = CurriculumnPlaner()
    planer.show()
    app.exec()

