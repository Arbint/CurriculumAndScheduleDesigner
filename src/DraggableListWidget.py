from PySide6.QtWidgets import QListWidget 
from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent
from PySide6.QtCore import Qt

class DraggeableListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)

    def startDrag(self, supportedActions: Qt.DropAction) -> None: 
        print(f"dragging started")
        super().startDrag(supportedActions)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        print(f"dragging enter!")
        event.accept()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        print(f"dragging moving evnet!!")
        event.accept()
        
    def dropEvent(self, event):
        self.addItem("hahah")
        event.setDropAction(Qt.MoveAction)