import requests
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import pyqtSignal

from ui.rooms_menu_ui import RoomMenu_UI

class RoomMenu(RoomMenu_UI):
    go_to_main_menu = pyqtSignal()
    join_successful = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)

        self.current_selected_room = None

        self.table.itemSelectionChanged.connect(self.on_room_selection_changed)
        self.btn_main_menu.clicked.connect(self.go_to_main_menu.emit)
        self.btn_create_room.clicked.connect(self.create_room)
        self.btn_join.clicked.connect(self.join_room)

        self.load_rooms()

    def load_rooms(self):
        try:
            # TO DO (Настроить подсоединение к системе #ВаляСкиньAPIGateway)
            # response = requests.get('http://.../rooms')
            # data = response.json()
            data = [
                {"name": "Комната Alpha", "participants": ["Alice", "Bob"]},
                {"name": "Комната Beta", "participants": ["Charlie"]},
                {"name": "Комната Gamma", "participants": []},
            ]
            self.update_table(data)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Ошибка соединения", f"Не удалось загрузить комнаты: {e}")
            self.update_table([])

    def on_room_selection_changed(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            self.current_selected_room = self.table.item(row, 0).text()
            self.btn_join.setEnabled(True)
        else:
            self.current_selected_room = None
            self.btn_join.setEnabled(False)

    def join_room(self):
        if not self.current_selected_room:
            return

        room_name = self.current_selected_room
        try:
            # TO DO (Настроить подсоединение к системе #ВаляСкиньAPIGateway)
            # payload = {'room_name': room_name}
            # response = requests.post('http://..../join', json=payload)
            # if response.status_code == 200:
            #     print("Успешное присоединение!")
            #     self.join_successful.emit(room_name)
            # else:
            #     QMessageBox.warning(self, "Ошибка", f"Не удалось присоединиться: {response.status_code}")
            QMessageBox.information(self, "Успех", f"Успешное присоединение к {room_name}! (заглушка)")
            self.join_successful.emit(room_name)
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Ошибка сети", f"Ошибка при отправке запроса: {e}")

    def create_room(self):
        try:
            # TO DO (Настроить подсоединение к системе #ВаляСкиньAPIGateway)
            # response = requests.post('http://.../create_room')
            # if response.status_code == 201:
            #     QMessageBox.information(self, "Успех", "Комната успешно создана!")
            #     self.load_rooms()
            # else:
            #     QMessageBox.warning(self, "Ошибка", "Не удалось создать комнату.")

            QMessageBox.information(self, "Успех", "Комната X успешно создана! (заглушка)")
            self.load_rooms()
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Ошибка сети", f"Ошибка при отправке запроса: {e}")

