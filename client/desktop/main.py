import sys
import asyncio

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from qasync import QEventLoop

from utils.client_websocket import ClientWebSocket
from windows.main_menu import MainMenu
from windows.rooms_menu import RoomMenu
from windows.singleplayer_editor import SinglePlayerEditorWindow
from windows.multiplayer_editor import MultiPlayerEditorWindow


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.CW = ClientWebSocket()

        self.setWindowTitle("OurPaint")
        self.setGeometry(600, 250, 800, 600)
        self.setStyleSheet(f"background-color: #333842; color: white;")

        self.main_menu = MainMenu(self)
        self.rooms_menu = RoomMenu(self, self.CW)
        self.CW.set_ROOM_MENU(self.rooms_menu)
        self.single_image_editor = SinglePlayerEditorWindow(self)
        self.multi_image_editor = MultiPlayerEditorWindow(self, self.CW)
        self.CW.set_MULTI_EDITOR(self.multi_image_editor)

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.rooms_menu)
        self.stacked_widget.addWidget(self.single_image_editor)
        self.stacked_widget.addWidget(self.multi_image_editor)

        self.main_menu.start_single_player.connect(self.show_single_editor)
        self.main_menu.start_multi_player.connect(self.show_rooms_menu)
        self.rooms_menu.go_to_main_menu.connect(self.show_main_menu)
        self.rooms_menu.open_multiplayer_editor.connect(self.show_multi_editor)
        self.single_image_editor.canvas.go_to_main_menu.connect(self.show_main_menu)
        self.multi_image_editor.canvas.go_to_main_menu.connect(self.show_rooms_menu)

    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)
        self.setGeometry(600, 250, 800, 600)
    def show_rooms_menu(self):
        self.stacked_widget.setCurrentWidget(self.rooms_menu)
        self.setGeometry(600, 250, 800, 600)
    def show_single_editor(self):
        self.stacked_widget.setCurrentWidget(self.single_image_editor)
        self.setGeometry(550, 200, 1000, 700)
    def show_multi_editor(self):
        self.stacked_widget.setCurrentWidget(self.multi_image_editor)
        self.setGeometry(550, 200, 1000, 700)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainApp()
    window.show()

    with loop:
        loop.run_forever()

