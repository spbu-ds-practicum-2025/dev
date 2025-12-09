from PyQt5 import uic
from PyQt5.QtWidgets import QDialog

class ConnectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("ui/server_connection_dialog.ui", self)

        self.connectButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)

    def get_values(self):
        return self.ipField.text(), int(self.portField.text())
