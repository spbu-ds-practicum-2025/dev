import json
import websockets
from websockets import ConnectionClosedError
from websockets.protocol import State
import asyncio

from PyQt6.QtWidgets import QMessageBox, QDialog
from PyQt6.QtCore import pyqtSignal
from qasync import asyncSlot

from ui.rooms_menu_ui import RoomMenu_UI
from .server_connection_dialog import ServerConnectionDialog
from .room_creation_dialog import RoomCreationDialog
from utils.client_websocket import ClientWebSocket

class RoomMenu(RoomMenu_UI):
    go_to_main_menu = pyqtSignal()
    open_multiplayer_editor = pyqtSignal()

    def __init__(self, parent, client_websocket: ClientWebSocket):
        super().__init__(parent)
        self.CW = client_websocket

        # ------------

        self.button_connect_to_server.clicked.connect(self.on_connect_button_clicked)
        self.table.itemSelectionChanged.connect(self.on_room_selection_changed)
        self.btn_main_menu.clicked.connect(self.go_to_main_menu.emit)
        self.btn_create_room.clicked.connect(self.on_create_room_button_clicked)
        self.btn_join.clicked.connect(self.on_join_room_button_clicked)

        self.update_table({})
        self.update_status_label(status="disconnected")

    @asyncSlot()
    async def on_connect_button_clicked(self):
        dialog = ServerConnectionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if self.CW.websocket and self.CW.websocket.state == State.OPEN:
                self.handle_result(f"Ошибка|Подключение к серверу уже установлено")
                return
            try:
                ip, port = dialog.get_input()
                self.update_status_label(status="connecting")
                websocket = await asyncio.wait_for(
                    websockets.connect(f'ws://{ip}:{port}/ws'),
                    timeout=10
                )
                self.CW.set_websocket(websocket)
                self.update_status_label(status="connected")
                await asyncio.gather(
                    self.update_rooms_data(),
                    self.send_heartbeat(),
                    self.CW.listen_server()
                )

            except ConnectionClosedError:
                self.handle_result(f"Ошибка|Сервер разорвал соединение. Проверьте состояние сервера.")
                if (not self.CW.websocket) or (self.CW.websocket and not self.CW.websocket.state == State.OPEN):
                    self.update_status_label(status="disconnected")
            except ConnectionRefusedError as e:
                self.handle_result(f"Ошибка|Не удалось подключиться к серверу.")
                if (not self.CW.websocket) or (self.CW.websocket and not self.CW.websocket.state == State.OPEN):
                    self.update_status_label(status="disconnected")
            except Exception as e:
                self.handle_result(f"Ошибка|Ошибка при подключении к серверу:{str(e)}")
                if (not self.CW.websocket) or (self.CW.websocket and not self.CW.websocket.state == State.OPEN):
                    self.update_status_label(status="disconnected")

    @asyncSlot()
    async def on_create_room_button_clicked(self):
        dialog = RoomCreationDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            if not (self.CW.websocket and self.CW.websocket.state == State.OPEN):
                self.handle_result("Ошибка|Отсутствует подключение к серверу")
                return

            self.update_status_label(status="processing")

            try:
                room_name = dialog.get_input()
                await self.CW.websocket.send(json.dumps({"type": "create_room", "room_name": room_name}))

            except asyncio.TimeoutError:
                self.handle_result("Ошибка|Таймаут при ожидании ответа.")
            except Exception as e:
                self.handle_result(f"Ошибка|Не удалось создать комнату: {e}")
            self.update_status_label(status="connected")

    @asyncSlot()
    async def on_join_room_button_clicked(self):
        if not self.current_selected_room:
            self.handle_result("Ошибка|Выберите комнату для подключения")
            return
        if not (self.CW.websocket and self.CW.websocket.state == State.OPEN):
            self.handle_result("Ошибка|Отсутствует подключение к серверу")
            return

        self.update_status_label(status="processing")
        try:
            room_name = self.current_selected_room
            data = {"type": "join_room", "room_name": room_name}
            await self.CW.websocket.send(json.dumps(data))
        except Exception as e:
            self.handle_result(f"Ошибка|Не удалось подключиться к комнате: {e}")
        self.update_status_label(status="connected")

    def open_multiplayer_editor_func(self):
        self.open_multiplayer_editor.emit()

    async def send_heartbeat(self):
        while self.CW.exist():
            try:
                await self.CW.websocket.ping()
                await asyncio.sleep(8)
            except Exception:
                self.update_status_label(status="disconnected")
                self.CW.websocket = None
                break

    async def update_rooms_data(self):
        if self.CW.websocket and self.CW.websocket.state == State.OPEN:
            try:
                data = {"type": "get_info"}
                await self.CW.websocket.send(json.dumps(data))
            except Exception as e:
                self.handle_result(f"Ошибка|Не удалось отправить запрос на получение данных: {e}")

    def handle_result(self, result):
        title, message = result.split('|')
        QMessageBox.information(self, title, message)
