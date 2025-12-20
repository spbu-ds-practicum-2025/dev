from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton

class ResizeDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Введите размеры нового изображения")

        self.layout = QFormLayout(self)

        self.width_input = QLineEdit(self)
        self.height_input = QLineEdit(self)

        self.layout.addRow("Ширина:", self.width_input)
        self.layout.addRow("Высота:", self.height_input)

        self.confirm_button = QPushButton("Создать", self)
        self.confirm_button.clicked.connect(self.accept)
        self.layout.addWidget(self.confirm_button)

    def get_input(self):
        width_input = self.width_input.text()
        height_input = self.height_input.text()
        width = int(width_input) if width_input.isdigit() else 16
        height = int(height_input) if height_input.isdigit() else 16
        return width, height
