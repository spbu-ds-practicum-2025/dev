from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class RoomsMenuWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        uic.loadUi("ui/rooms_menu.ui", self)

        self.refreshButton.clicked.connect(self.refresh_rooms)
        self.joinButton.clicked.connect(self.join_room)
        self.createButton.clicked.connect(self.create_room)
        self.backButton.clicked.connect(self.go_back)

    def refresh_rooms(self):
        pass

    def join_room(self):
        self.app.stack.setCurrentWidget(self.app.editorMulti)

    def create_room(self):
        self.app.stack.setCurrentWidget(self.app.editorMulti)

    def go_back(self):
        self.app.stack.setCurrentWidget(self.app.mainMenu)
