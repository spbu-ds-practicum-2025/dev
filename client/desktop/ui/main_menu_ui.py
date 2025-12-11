from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class MainMenu_UI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("OurPaint")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #2c2f36;")

        title_label = QLabel("OurPaint", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font: 30pt 'Baskerville Old Face'; color: white;")

        self.single_player_button = QPushButton("Однопользовательское\nредактирование", self)
        self.single_player_button.setStyleSheet("font: 14pt 'Franklin Gothic Medium'; background-color: #444c56; color: white;")
        self.single_player_button.setFixedSize(250, 50)

        self.multi_player_button = QPushButton("Многопользовательское\nредактирование", self)
        self.multi_player_button.setStyleSheet("font: 14pt 'Franklin Gothic Medium'; background-color: #444c56; color: #EEEEEE;")
        self.multi_player_button.setFixedSize(250, 50)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.single_player_button)
        layout.addWidget(self.multi_player_button)
        self.setLayout(layout)
