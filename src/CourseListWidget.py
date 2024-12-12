from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QListView, QLabel, QListWidget, QMenu, QAbstractItemView
from PySide6.QtCore import Qt, QMimeData, QModelIndex, QPoint, Signal
from PySide6.QtGui import QDrag, QPixmap, QPainter, QDragEnterEvent, QDragMoveEvent, QDropEvent, QAction
from CourseConfigureWidget import CourseConfigureWidget
from CourseList import CourseListModel
from Course import Course
import pickle

class CouresListView(QListView):
    courseDuplicated = Signal(Course)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.ShowContextMenu)

    def ShowContextMenu(self, position: QPoint):
        index = self.indexAt(position)
        if index.isValid():
            contextMenu = QMenu(self)
            changeAction = QAction("Configure")
            deleteAction = QAction("Delete")
            duplicateAction = QAction("Duplicate")

            contextMenu.addAction(changeAction)
            contextMenu.addAction(deleteAction)
            contextMenu.addAction(duplicateAction)
            
            changeAction.triggered.connect(lambda : self.ChangeCourse(index))
            deleteAction.triggered.connect(lambda : self.DeleteCourse(index))
            duplicateAction.triggered.connect(lambda : self.DuplicateCourse(index))
            contextMenu.exec(self.viewport().mapToGlobal(position))

    def DuplicateCourse(self, courseIndex):
        courseToDuplicate : Course = self.model().data(courseIndex, Qt.UserRole)
        self.courseDuplicated.emit(courseToDuplicate)

    def ChangeCourse(self, courseIndex):
        courseToConfigure : Course = self.model().data(courseIndex, Qt.UserRole)
        configureWidget = CourseConfigureWidget(self, CourseConfigureWidget.ConfigureMode(), courseToConfigure)
        configureWidget.onConfigureCourse.connect(self.CourseConfigured)

    def CourseConfigured(self):
        self.model().layoutChanged()

    def DeleteCourse(self, courseIndex):
        self.model().removeRow(courseIndex.row(), QModelIndex())


class CourseListViewGroup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.nameLabel = QLabel("")
        self.listView = CouresListView() 
        self.listView.clicked.connect(self.ItemClicked)

        self.masterLayout.addWidget(self.nameLabel)
        self.masterLayout.addWidget(self.listView)

        self.totalCreditsLabel = QLabel("")
        self.masterLayout.addWidget(self.totalCreditsLabel)

        self.courseListModel = None

    def BindModel(self, modelToBind: CourseListModel):
        self.nameLabel.setText(modelToBind.listName)
        self.listView.setModel(modelToBind)
        self.courseListModel = modelToBind
        self.courseListModel.selectionChanged.connect(self.UpdateSelectionToIndex)
        self.courseListModel.layoutChanged.connect(self.ModelUpdated)
        self.UpdateCredits()


    def UpdateSelectionToIndex(self, index: QModelIndex):
        selectionMode = self.listView.selectionMode()
        if selectionMode:
            self.listView.setCurrentIndex(index)


    def ItemClicked(self, index):
        itemData : Course = self.listView.model().data(index, Qt.UserRole)
        itemData.finished = not itemData.finished
        self.courseListModel.dataChanged.emit(index, index)


    def ModelUpdated(self):
        self.UpdateCredits()

    def UpdateCredits(self):
        self.totalCreditsLabel.setText(f"Total Credits: {self.courseListModel.GetTotalCredits()}")


