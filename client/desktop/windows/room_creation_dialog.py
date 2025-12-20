from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton

class RoomCreationDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Введите название комнаты")

        self.layout = QFormLayout(self)

        self.room_name_input = QLineEdit(self)
        self.room_name_input.setText("Тест")
        self.layout.addRow("Название комнаты:", self.room_name_input)

        self.confirm_button = QPushButton("Создать", self)
        self.confirm_button.clicked.connect(self.accept)
        self.layout.addWidget(self.confirm_button)

    def get_input(self):
        room_name = self.room_name_input.text().strip()
        return room_name
