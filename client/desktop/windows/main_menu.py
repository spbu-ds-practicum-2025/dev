from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QDialog

from .connection_dialog import ConnectionDialog

class MainMenuWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        uic.loadUi("ui/main_menu.ui", self)

        self.singleButton.clicked.connect(self.go_single)
        self.multiButton.clicked.connect(self.go_multi)
        self.exitButton.clicked.connect(self.exit_app)

    def go_single(self):
        self.app.stack.setCurrentWidget(self.app.editorSingle)

    def go_multi(self):
        dialog = ConnectionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            ip, port = dialog.get_values()
            self.app.stack.setCurrentWidget(self.app.roomsMenu)

    def exit_app(self):
        self.app.app.quit()
