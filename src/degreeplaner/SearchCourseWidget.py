from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel
from PySide6.QtCore import Signal, Qt

class SearchCourseWidget(QWidget):
    startSearch = Signal(str)

    def __init__(self, parent = None):
        super().__init__(parent = parent)
        self.setMinimumSize(400, 200)
        self.setWindowFlags(Qt.WindowType.Window)
        self.setWindowTitle("Search Course")

        masterLayout = QVBoxLayout()
        self.setLayout(masterLayout)
        searchConfigLayout = QGridLayout()
        masterLayout.addLayout(searchConfigLayout)

        searchConfigLayout.addWidget(QLabel("Name:"), 0, 0)
        self.searchKeywordLineEdit = QLineEdit()
        searchConfigLayout.addWidget(self.searchKeywordLineEdit, 0, 1)

        searchBtn = QPushButton("Search")
        searchBtn.clicked.connect(self.SearchBtnClicked)
        masterLayout.addWidget(searchBtn)

        quitBtn = QPushButton("Quit")
        quitBtn.clicked.connect(lambda : self.close())
        masterLayout.addWidget(quitBtn)

        self.show()

    def SearchBtnClicked(self):
        searchKeyword = self.searchKeywordLineEdit.text()
        self.startSearch.emit(searchKeyword)