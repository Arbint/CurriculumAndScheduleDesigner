from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QListView
from PySide6.QtCore import QAbstractListModel

class ListModel(QAbstractListModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()]

    def flags(self, index):
        default_flags = super().flags(index)
        return default_flags | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled

    def mimeTypes(self):
        return ["application/x-qabstractitemmodeldatalist"]

    def mimeData(self, indexes):
        mime_data = QMimeData()
        encoded_data = [index.row() for index in indexes]
        mime_data.setData("application/x-qabstractitemmodeldatalist", str(encoded_data).encode())
        return mime_data

    def dropMimeData(self, data, action, row, column, parent):
        if action == Qt.IgnoreAction:
            return True

        if not data.hasFormat("application/x-qabstractitemmodeldatalist"):
            return False

        encoded_data = data.data("application/x-qabstractitemmodeldatalist")
        moved_rows = eval(encoded_data.decode())

        if row < 0:
            row = self.rowCount()

        for moved_row in moved_rows:
            item = self._data.pop(moved_row)
            self._data.insert(row, item)

        self.dataChanged.emit(self.index(0, 0), self.index(self.rowCount() - 1, 0))

        return True

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])
    model = ListModel(["Item 1", "Item 2", "Item 3"])
    view = QListView()
    view.setDragEnabled(True)
    view.setAcceptDrops(True)
    view.setDropIndicatorShown(True)
    view.setModel(model)
    view.show()
    app.exec()