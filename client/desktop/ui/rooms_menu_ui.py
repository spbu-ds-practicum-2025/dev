from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,
    QHBoxLayout, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QPushButton, QHeaderView,
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

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Название комнаты', 'Участники'])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().hide()

        self.btn_main_menu = QPushButton("← В главное меню")
        self.btn_create_room = QPushButton("Создать комнату")
        self.btn_join = QPushButton("Присоединиться")
        self.btn_join.setEnabled(False)

        self.table.setStyleSheet(f"background-color: {color1};")
        self.table.horizontalHeader().setStyleSheet(f"QHeaderView::section {{ background-color: {color2}; color: white; }}")
        self.table.verticalHeader().setStyleSheet(f"QHeaderView::section {{ background-color: {color2}; color: white; }}")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.btn_main_menu)
        button_layout.addStretch(1)
        button_layout.addWidget(self.btn_create_room)
        button_layout.addWidget(self.btn_join)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def update_table(self, rooms_data):
        row_count = len(rooms_data)
        self.table.setRowCount(row_count)
        for row, room in enumerate(rooms_data):
            self.table.setItem(row, 0, QTableWidgetItem(room["name"]))
            participants_str = ", ".join(room["participants"])
            self.table.setItem(row, 1, QTableWidgetItem(participants_str))
        self.table.resizeColumnsToContents()


