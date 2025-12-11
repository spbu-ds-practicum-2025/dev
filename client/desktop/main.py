import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from windows.main_menu import MainMenu
from windows.rooms_menu import RoomMenu
from windows.editor import EditorWindow

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OurPaint")
        self.setGeometry(600, 250, 800, 600)
        self.setStyleSheet(f"background-color: #333842; color: white;")

        self.main_menu = MainMenu(self)
        self.rooms_menu = RoomMenu(self)
        self.image_editor = EditorWindow(self)

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.rooms_menu)
        self.stacked_widget.addWidget(self.image_editor)

        self.main_menu.start_single_player.connect(self.show_editor)
        self.main_menu.start_multi_player.connect(self.show_rooms_menu)
        self.rooms_menu.go_to_main_menu.connect(self.show_main_menu)
        self.image_editor.canvas.go_to_main_menu.connect(self.show_main_menu)

    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)
        self.setGeometry(600, 250, 800, 600)
    def show_editor(self):
        self.stacked_widget.setCurrentWidget(self.image_editor)
        self.setGeometry(550, 200, 1000, 700)
    def show_rooms_menu(self):
        self.stacked_widget.setCurrentWidget(self.rooms_menu)
        self.setGeometry(600, 250, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
