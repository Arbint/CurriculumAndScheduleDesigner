from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog
from PySide6.QtGui import QAction
from CourseListWidget import CourseListViewGroup
from CourseList import CourseListModel
from Course import Course
import os
import SaveUtilties

class CurriculumnPlaner(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ConfigureMainMenu()
        self.setCentralWidget(QWidget())
        self.centralMasterLayout = QHBoxLayout()
        self.centralWidget().setLayout(self.centralMasterLayout)

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
        self.centralMasterLayout.addWidget(self.allClassListViewGrp)
        self.models[self.GetAllClassesNameStr()] = self.allClassModel

    def ConfigureFinishedClassList(self):
        self.finishedClassListViewGrp = CourseListViewGroup()
        self.finishedClassModel = CourseListModel([], self.GetFinishedClassesNameStr())
        self.finishedClassListViewGrp.BindModel(self.finishedClassModel)
        self.centralMasterLayout.addWidget(self.finishedClassListViewGrp)
        self.models[self.GetFinishedClassesNameStr()] = self.finishedClassModel

    def AddSemester(self, name: str, parentGrid: QGridLayout, x, y, semesterCourses : list[Course] = None):
        semesterView = CourseListViewGroup()
        semesterModel = CourseListModel(semesterCourses, name)
        semesterView.BindModel(semesterModel)
        parentGrid.addWidget(semesterView, x, y)
        self.semestersModels[name] = semesterModel
        self.models[name] = semesterModel

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


    def GetAllClassesNameStr(self):
        return "All Classes"

    def GetFinishedClassesNameStr(self):
        return "Finished Classes"

if __name__ == "__main__":
    app = QApplication()
    planer = CurriculumnPlaner()
    planer.show()
    app.exec()

