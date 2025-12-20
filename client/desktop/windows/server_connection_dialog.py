from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton

class ServerConnectionDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Введите IP/Порт для подключение к серверу")

        self.layout = QFormLayout(self)

        self.ip_input = QLineEdit(self)
        self.ip_input.setText("192.168.0.12")
        self.port_input = QLineEdit(self)
        self.port_input.setText("8080")
        self.layout.addRow("IP:", self.ip_input)
        self.layout.addRow("Port:", self.port_input)

        self.confirm_button = QPushButton("Подключиться", self)
        self.confirm_button.clicked.connect(self.accept)
        self.layout.addWidget(self.confirm_button)

    def get_input(self):
        ip = self.ip_input.text().strip()
        port = self.port_input.text().strip()
        return ip, port
