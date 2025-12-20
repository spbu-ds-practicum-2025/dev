from PyQt6.QtWidgets import QFrame, QPushButton, QLabel

from .singleplayer_editor_ui import SinglePlayerEditorUI

color1 = "#555a64"
color2 = "#444953"
color2_1 = "#444c56"
color3 = "#333842"

class MultiPlayerEditorUI(SinglePlayerEditorUI):
    def __init__(self, parent):
        super().__init__(parent)

        e1 = QFrame()
        e1.setMinimumHeight(15)
        self.role_status_label = QLabel("  Роль редактора:\n  <Ожидание>")
        e2 = QFrame()
        e2.setMinimumHeight(5)
        self.btn_take_role = QPushButton("Занять роль")
        self.btn_leave_role = QPushButton("Освободить роль")

        self.redactor_layout.addStretch()
        self.redactor_layout.addWidget(self.role_status_label)
        self.redactor_layout.addWidget(e1)
        self.redactor_layout.addWidget(self.btn_take_role)
        self.redactor_layout.addWidget(self.btn_leave_role)
        self.redactor_layout.addWidget(e2)



