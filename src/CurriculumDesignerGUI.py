from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QGridLayout, QPushButton
import CurriculumDesigner

class CurriculumnDesignerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Curriculumn Designer")

if __name__ == "__main__":
    app = QApplication()
    window = CurriculumnDesignerWindow()
    window.show()
    app.exec()