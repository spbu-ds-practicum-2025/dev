from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QPushButton, QHeaderView, QLabel,
)

color1 = "#555a64"
color2 = "#444953"
color2_1 = "#444c56"
color3 = "#333842"

class RoomMenu_UI(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Выбор Комнаты (PyQT6)")
        self.setGeometry(100, 100, 600, 400)

        self.button_connect_to_server = QPushButton("Подключиться к серверу")
        self.button_connect_to_server.setMaximumWidth(150)
        self.status_label = QLabel(f"Статус соединения: <span style='color: red;'>нет соединения с сервером</span>")
        # self.button_ask_server_data = QPushButton("Запросить инфу")

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Название комнаты', 'Участники'])
        self.table.setColumnWidth(0, 135)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().hide()

        self.btn_main_menu = QPushButton("← В главное меню")
        self.btn_create_room = QPushButton("Создать комнату")
        self.btn_join = QPushButton("Присоединиться к комнате")
        self.btn_join.setEnabled(False)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.button_connect_to_server, alignment=Qt.AlignmentFlag.AlignLeft)
        top_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignRight)
        # top_layout.addWidget(self.button_ask_server_data)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_main_menu)
        button_layout.addStretch(1)
        button_layout.addWidget(self.btn_create_room)
        button_layout.addWidget(self.btn_join)
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.table.setStyleSheet(f"background-color: {color1};")
        self.table.horizontalHeader().setStyleSheet(f"QHeaderView::section {{ background-color: {color2}; color: white; }}")
        self.table.verticalHeader().setStyleSheet(f"QHeaderView::section {{ background-color: {color2}; color: white; }}")

    def update_table(self, rooms_data):
        row_count = len(rooms_data)
        self.table.setRowCount(row_count)
        for row, room in enumerate(list(rooms_data.keys())):
            self.table.setItem(row, 0, QTableWidgetItem(room))
            participants_str = ", ".join(rooms_data[room])
            self.table.setItem(row, 1, QTableWidgetItem(participants_str))
        # self.table.resizeColumnsToContents()


