from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class SingleEditorWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        uic.loadUi("ui/editor_single.ui", self)
        self.app = app
