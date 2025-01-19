from Course import Course
from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, QMimeData, Signal 
from PySide6.QtGui import QImage
import AssetManager
import pickle

class CourseListModel(QAbstractListModel):
    selectionChanged = Signal(QModelIndex)
    def __init__(self, initCourses: list[Course] = None, initListName: str = "", parent=None):
        super().__init__(parent)

        self.listName= initListName
        self.courses = initCourses if initCourses != None else []
        self.tick = QImage(AssetManager.GetFinishedIcon())

    def AddNewCourse(self, courseDepartmentPrefix, courseNumber, courseName, courseFinished, courseNote):
        self.courses.append(Course(courseDepartmentPrefix, courseNumber, courseName, courseFinished, courseNote))
        self.layoutChanged.emit()

    def DuplicateCourse(self, courseToDuplicate: Course):
        self.courses.append(courseToDuplicate.MakeDuplicate())
        self.layoutChanged.emit()

    def SelectWithKeyword(self, keyword: str):
        for row in range(self.rowCount()):
            index = self.index(row, 0)
            itemText = self.data(index, Qt.DisplayRole)
            if keyword.lower() in itemText.lower():
                self.selectionChanged.emit(index)

    def Clear(self):
        self.beginResetModel()
        self.courses = []
        self.endResetModel()

    def InitCoursesFromList(self, courseList):
        for courseDict in courseList:
            newCourse = Course.CreateFromDict(courseDict)
            self.courses.append(newCourse)
        
        self.layoutChanged.emit()
        
    def CoursesToJsonList(self):
        outCourses = []
        for course in self.courses:
            outCourses.append(course.ToInfoDict())

        return outCourses

    def GetTotalCredits(self):
        credits = 0
        for course in self.courses:
            credits += course.GetCredits()

        return credits

    def rowCount(self, parent = None):
        return len(self.courses)


    def data(self, index, role):
        course = self.courses[index.row()]
        if role == Qt.DisplayRole:
            return f"{course}" 
        
        if role == Qt.UserRole:
            return course

        if role == Qt.DecorationRole:
            if course.finished:
                return self.tick

    def supportedDragActions(self):
        return Qt.MoveAction

    def supportedDropActions(self):
        return Qt.MoveAction 

    # needed to support the mime types, other wise, the drag and drop will not work
    def mimeTypes(self):
        return [CourseListModel.GetMimeDataFormat()]
        
    def flags(self, index):
        defaultFlags = super().flags(index)
        return defaultFlags | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled

    def mimeData(self, indexes):
        mimeData = QMimeData()
        if indexes:
            course = self.data(indexes[0], Qt.UserRole)
            mimeData.setData(CourseListModel.GetMimeDataFormat(), pickle.dumps(course))

            mimeData.sourceModel = self
            mimeData.sourceIndex = indexes[0]

        return mimeData

    def dropMimeData(self, data, action, row, column, parent):
        if not data.hasFormat(CourseListModel.GetMimeDataFormat()):
            return False

        if action == Qt.MoveAction:
            srcModel: CourseListModel = data.sourceModel
            srcIndex = data.sourceIndex
            srcModel.removeRow(srcIndex.row(), QModelIndex())

            course = pickle.loads(data.data(CourseListModel.GetMimeDataFormat()))
            self.courses.insert(row, course)
            self.layoutChanged.emit()

            return True

    def removeRow(self, row, parent):
        if 0 <= row and row < len(self.courses):
            self.beginRemoveRows(parent, row, row)
            del self.courses[row]
            self.endRemoveRows()
            self.layoutChanged.emit()
            return True

        return False

    @staticmethod
    def GetMimeDataFormat():
        return "application/x-course"