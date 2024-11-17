from PySide6.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDrag, QPixmap, QPainter
from PySide6.QtCore import Qt, QMimeData
from Course import Course
import pickle

class CourseListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def startDrag(self, supportedActions: Qt.DropAction) -> None: 
        item = self.currentItem()
        if item is None:
            return

        drag = QDrag(self)
        mimeData = QMimeData()
        course = item.data(Qt.UserRole)
        mimeData.setData(CourseListWidget.GetDragMimeDataFormat(), pickle.dumps(course))
        drag.setMimeData(mimeData)

        text = item.text()
        index = self.indexFromItem(item)
        rect = self.visualRect(index)
        pixmap = QPixmap(rect.size())
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setPen(Qt.green)
        painter.setFont(self.font())
        painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(pixmap.rect().center())

    
        if drag.exec(Qt.MoveAction) == Qt.MoveAction:
            self.takeItem(self.row(item))
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(CourseListWidget.GetDragMimeDataFormat()):
            event.acceptProposedAction()
        else:
            super().dragEngerEvent(event)
        
    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat(CourseListWidget.GetDragMimeDataFormat()):
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasFormat(CourseListWidget.GetDragMimeDataFormat()):
            course = pickle.loads(event.mimeData().data(CourseListWidget.GetDragMimeDataFormat()))
            self.AddCourse(course)
            event.acceptProposedAction()

    def SetCourses(self, courses: list[Course]):
        for course in courses:
            self.AddCourse(course)

    def AddCourse(self, course: Course):
        courseStr = f"{course}"
        print(f"adding course {courseStr}")
        item = QListWidgetItem(courseStr)
        item.setData(Qt.UserRole, course)
        self.addItem(item)

    def GetCourses(self)->list[Course]:
        courses = []
        for item in self.items():
            courses.append(item.data(Qt.UserRole))

        return courses

    @staticmethod
    def GetDragMimeDataFormat():
        return "application/x-course"