from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QSplitter, QVBoxLayout, QWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adjustable Layout Example")

        # Create widgets
        label1 = QLabel("Widget 1")
        label1.setStyleSheet("background-color: lightblue;")
        label2 = QLabel("Widget 2")
        label2.setStyleSheet("background-color: lightgreen;")
        label3 = QLabel("Widget 3")
        label3.setStyleSheet("background-color: lightcoral;")

        # Add widgets to a QSplitter
        splitter = QSplitter()
        splitter.addWidget(label1)
        splitter.addWidget(label2)
        splitter.addWidget(label3)

        # Layout to contain the QSplitter
        layout = QVBoxLayout()
        layout.addWidget(splitter)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
