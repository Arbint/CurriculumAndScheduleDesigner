from Course import Course
from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, QMimeData
import pickle

class CourseListModel(QAbstractListModel):
    def __init__(self, initCourse: list[Course] = [], initListName: str = "", parent=None):
        super().__init__(parent)

        self.listName= initListName
        self.courses = initCourse 


    def rowCount(self, parent):
        return len(self.courses)


    def data(self, index, role):
        course = self.courses[index.row()]
        if role == Qt.DisplayRole:
            return f"{course}" 
        
        if role == Qt.UserRole:
            return course

        
    def flags(self, index):
        defaultFlags = super().flags(index)

        if(index.isValid()):
            return defaultFlags | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled
        else:
            return defaultFlags | Qt.ItemIsDropEnabled


    def mimeData(self, indexes):
        mimeData = QMimeData()
        if indexes:
            course = self.data(indexes[0], Qt.UserRole)
            mimeData.setData(CourseListModel.GetMimeDataFormat(), pickle.dumps(course))

        return mimeData
    

    def dropMimeData(self, data, action, row, column, parent):
        if not data.hasFormat(CourseListModel.GetMimeDataFormat()):
            return False

        course = pickle.loads(data.data(CourseListModel.GetMimeDataFormat()))
        if row >= 0 and row <= len(self.courses):
            self.courses.insert(row, course)
            self.layoutChanged.emit()
            return True

        return False
       
    def supportedDragActions(self):
        return Qt.MoveAction
    
    def removeRow(self, row, parent):
        if 0 <= row and row < len(self.courses):
            del self.courses[row]
            self.layoutChanged.emit()
            return True

        return False

    @staticmethod
    def GetMimeDataFormat():
        return "application/x-course"

