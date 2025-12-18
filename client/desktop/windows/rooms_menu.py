import requests
from PyQt6.QtWidgets import QMessageBox, QDialog
from PyQt6.QtCore import pyqtSignal

from ui.rooms_menu_ui import RoomMenu_UI
from utils.thread_worker import ThreadWorker
from .server_connection_dialog import ServerConnectionDialog

class RoomMenu(RoomMenu_UI):
    go_to_main_menu = pyqtSignal()
    join_successful = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        # ------------
        self.server_ip = None
        self.server_port = None
        self.is_connected = False
        # ------------

        self.current_selected_room = None

        self.button_connect_to_server.clicked.connect(self.open_connect_to_server_dialog)
        # self.button_ask_server_data.clicked.connect(self.update_rooms_data)
        self.table.itemSelectionChanged.connect(self.on_room_selection_changed)
        self.btn_main_menu.clicked.connect(self.go_to_main_menu.emit)
        self.btn_create_room.clicked.connect(self.create_room)
        self.btn_join.clicked.connect(self.join_room)

        self.update_table({})

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
            #     self.update_table({})
            # else:
            #     QMessageBox.warning(self, "Ошибка", "Не удалось создать комнату.")

            QMessageBox.information(self, "Успех", "Комната X успешно создана! (заглушка)")
            self.update_table({})
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Ошибка сети", f"Ошибка при отправке запроса: {e}")

    def open_connect_to_server_dialog(self):
        dialog = ServerConnectionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            ip, port = dialog.get_input()
            self.server_ip = ip
            self.server_port = port
            # self.connect_to_server(ip, port)

            url = f"http://{ip}:{port}/connect_client"
            print(f"Connecting to: {url}")
            self.do_async_request(self.connect_request, url)

    # def connect_to_server(self, server_ip, server_port):
    #     url = f"http://{server_ip}:{server_port}/connect_client"
    #     print(f"Connecting to: {url}")
    #
    #     self.worker = ThreadWorker(self.make_connect_request, url)
    #     self.worker.finished.connect(self.handle_result)
    #     self.worker.start()


    def update_rooms_data(self):
        print(self.server_port,self.server_ip, self.is_connected)
        if self.server_port and self.server_ip: # and self.is_connected:
            url = f"http://{self.server_ip}:{self.server_port}/update_rooms_data"
            print(f"Asking for data: {url}")

            self.do_async_request(self.data_request, url)


    def create_room(self, room_name):
        if self.server_port and self.server_ip: # and self.is_connected:
            url = f"http://{self.server_ip}:{self.server_port}/create_room/{'AAA'}"
            print(f"Asking for data: {url}")

            try:
                response = requests.post(url, timeout=3)
                if response.status_code == 200:
                    print(f"Успех|Комната успешно создана")
                else:
                    print(f"Ошибка|Ошибка сервера: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при создании комнаты|Непредвиденная ошибка: {e}")

            self.update_rooms_data()

    def do_async_request(self, function, url):
        if function and url:
            self.worker = ThreadWorker(function, url)
            self.worker.finished.connect(self.handle_result)
            self.worker.start()

    def data_request(self, url):
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                rooms_data = response.json()
                self.update_table(rooms_data["rooms"])
                return f"Успех|Информация получена: {rooms_data}"
            else:
                self.update_table({})
                return f"Ошибка|Ошибка сервера: {response.text}"
        except requests.exceptions.RequestException as e:
            return f"Ошибка при запросе информации с сервера|Непредвиденная ошибка: {e}"

    def connect_request(self, url):
        try:
            # self.is_connected = False
            response = requests.post(url, timeout=3)
            if response.status_code == 200:
                self.is_connected = True
                return "Успех|Успешное присоединение!"
            else:
                # self.server_ip = None
                # self.server_port = None
                return f"Ошибка|Ошибка сервера: {response.text}"
        except requests.exceptions.Timeout:
            # self.server_ip = None
            # self.server_port = None
            return "Ошибка при подключении к серверу|Время ожидания истекло. Проверьте введённый порт и IP."
        except requests.exceptions.ConnectionError:
            # self.server_ip = None
            # self.server_port = None
            return "Ошибка при подключении к серверу|Не удалось подключиться к серверу, проверьте состояние сервера."
        except requests.exceptions.RequestException as e:
            # self.server_ip = None
            # self.server_port = None
            return f"Ошибка при подключении к серверу|Непредвиденная ошибка: {e}"


    def handle_result(self, result):
        title, message = result.split('|')
        QMessageBox.information(self, title, message)

