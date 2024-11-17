from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QListView, QLabel, QListWidget
from PySide6.QtCore import Qt, QMimeData, QModelIndex
from PySide6.QtGui import QDrag, QPixmap, QPainter, QDragEnterEvent, QDragMoveEvent, QDropEvent
from CourseList import CourseListModel
from Course import Course
import pickle

class CouresListView(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)


    def startDrag(self, supportedActions):
        index = self.currentIndex()
        if not index.isValid():
            return

        course = index.data(Qt.UserRole)
        if not course:
            return

        mimeData = QMimeData() 
        mimeData.setData(CourseListModel.GetMimeDataFormat(), pickle.dumps(course))
        pixMap = self.generateDragPixMap(index, course)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixMap)
        drag.setHotSpot(pixMap.rect().center())

        if drag.exec(Qt.MoveAction) == Qt.MoveAction:
            self.model().removeRow(index.row(), QModelIndex())


    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasFormat(CourseListModel.GetMimeDataFormat()):
            event.acceptProposedAction()
        else:
            super().dragEnterEvent(event)


    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasFormat(CourseListModel.GetMimeDataFormat()):
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

        
    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasFormat(CourseListModel.GetMimeDataFormat()):
            mimeData = event.mimeData()
            self.model().dropMimeData(mimeData, event.dropAction(), self.model().rowCount(QModelIndex()), 0, QModelIndex())
            event.acceptProposedAction()

        else:
            super().dropEvent(event)


    def generateDragPixMap(self, index, courseItem: Course):
        rect = self.visualRect(index)
        pixMap = QPixmap(rect.size())
        pixMap.fill(Qt.transparent)

        painter = QPainter(pixMap)
        painter.setPen(Qt.green)
        painter.setFont(self.font())
        painter.drawText(pixMap.rect(), Qt.AlignCenter, f"{courseItem}")
        painter.end()
        return pixMap


class CourseListViewGroup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.label = QLabel("")
        self.listView = CouresListView() 

        self.listView.setDragEnabled(True)
        self.listView.setAcceptDrops(True)
        self.listView.setDropIndicatorShown(True)
        self.listView.setDefaultDropAction(Qt.MoveAction)

        self.masterLayout.addWidget(self.label)
        self.masterLayout.addWidget(self.listView)

    def BindModel(self, modelToBind: CourseListModel):
        self.label.setText(modelToBind.listName)
        self.listView.setModel(modelToBind)
