from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QListView, QLabel, QListWidget
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QPixmap, QPainter, QDragEnterEvent, QDragMoveEvent, QDropEvent
from CourseList import CourseListModel

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

        mimeData = self.model().mimeData([index]) 


class CourseListViewGroup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.label = QLabel("")
        self.listView = QListView() 

        self.listView.setDragEnabled(True)
        self.listView.setAcceptDrops(True)
        self.listView.setDropIndicatorShown(True)
        self.listView.setDefaultDropAction(Qt.MoveAction)

        self.masterLayout.addWidget(self.label)
        self.masterLayout.addWidget(self.listView)

    def BindModel(self, modelToBind: CourseListModel):
        self.label.setText(modelToBind.listName)
        self.listView.setModel(modelToBind)
