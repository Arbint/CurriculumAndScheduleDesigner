from PySide6.QtWidgets import QApplication, QListWidget, QListWidgetItem, QMainWindow
from PySide6.QtCore import Qt

class DraggableListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)  # Enable dragging
        self.setAcceptDrops(True)  # Allow dropping
        self.setDropIndicatorShown(True)  # Show drop indicator
        self.setDefaultDropAction(Qt.MoveAction)  # Default action for dropping

    def dragEnterEvent(self, event):
        # Accept the drag event if data is compatible
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        # Accept the drag move event
        event.accept()

    def dropEvent(self, event):
        # Handle drop event
        if event.mimeData().hasText():
            text = event.mimeData().text()
            self.addItem(text)  # Add the dropped item as a new list item
            event.accept()
        else:
            event.ignore()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drag-and-Drop QListWidget")
        self.setGeometry(100, 100, 400, 300)

        # Create the draggable list widget
        list_widget = DraggableListWidget()

        # Populate the list widget with sample items
        for i in range(5):
            item = QListWidgetItem(f"Item {i + 1}")
            list_widget.addItem(item)

        self.setCentralWidget(list_widget)


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
