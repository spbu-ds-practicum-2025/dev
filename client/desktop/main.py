import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget

from windows.main_menu import MainMenuWindow
from windows.rooms_menu import RoomsMenuWindow
from windows.editor_single import SingleEditorWindow
from windows.editor_multi import MultiEditorWindow

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.stack = QStackedWidget()

        self.mainMenu = MainMenuWindow(self)
        self.roomsMenu = RoomsMenuWindow(self)
        self.editorSingle = SingleEditorWindow(self)
        self.editorMulti = MultiEditorWindow(self)

        self.stack.addWidget(self.mainMenu)
        self.stack.addWidget(self.roomsMenu)
        self.stack.addWidget(self.editorSingle)
        self.stack.addWidget(self.editorMulti)

        self.stack.setCurrentWidget(self.mainMenu)
        self.stack.setFixedSize(1280, 720)
        self.stack.show()

    def run(self):
        self.app.exec_()

if __name__ == "__main__":
    App().run()
