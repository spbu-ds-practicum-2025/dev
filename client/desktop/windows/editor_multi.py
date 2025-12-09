from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class MultiEditorWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        uic.loadUi("ui/editor_multi.ui", self)
        self.app = app
