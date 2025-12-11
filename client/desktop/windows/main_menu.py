from PyQt6.QtCore import pyqtSignal

from ui.main_menu_ui import MainMenu_UI

class MainMenu(MainMenu_UI):
    start_single_player = pyqtSignal()
    start_multi_player = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)

        self.single_player_button.clicked.connect(self.start_single_player.emit)
        self.multi_player_button.clicked.connect(self.start_multi_player.emit)
