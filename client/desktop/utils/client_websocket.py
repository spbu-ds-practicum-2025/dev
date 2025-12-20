import asyncio
import base64
import json

from PyQt6.QtCore import QByteArray
from PyQt6.QtGui import QImage


class ClientWebSocket():
    def __init__(self):
        self.websocket = None
        self.lock = asyncio.Lock()

        self.ROOM_MENU = None
        self.MULTI_EDITOR = None

    def set_websocket(self, websocket):
        self.websocket = websocket

    def exist(self) -> bool:
        return self.websocket is not None

    def set_ROOM_MENU(self, ROOM_MENU):
        self.ROOM_MENU = ROOM_MENU

    def set_MULTI_EDITOR(self, MULTI_EDITOR):
        self.MULTI_EDITOR = MULTI_EDITOR

    async def listen_server(self):
        async for message in self.websocket:
            try:
                data = json.loads(message)

                # -------------- ROOMS-MENU ---------------

                if data["type"] == "get_info":
                    self.ROOM_MENU.update_table(data["data"]["rooms"])

                elif data["type"] == "create_room":
                    if data["status"] == "success":
                        await asyncio.create_task(self.ROOM_MENU.update_rooms_data())
                        self.ROOM_MENU.open_multiplayer_editor_func()
                        await self.websocket.send(json.dumps({"type": "get_image"}))
                        self.MULTI_EDITOR.stun_role_label()
                    elif data["status"] == "fail":
                        detail = data["detail"]
                        if detail == "already_exists":
                            self.ROOM_MENU.handle_result(f"Ошибка|Комната с этим именем уже существует")
                        if detail == "no_server":
                            self.ROOM_MENU.handle_result(f"Ошибка|Нет свободных серверов")
                        else:
                            self.ROOM_MENU.handle_result(f"Ошибка|Ошибка при создании комнаты: {detail}")

                elif data["type"] == "join_room":
                    if data["status"] == "success":
                        await asyncio.create_task(self.ROOM_MENU.update_rooms_data())
                        self.ROOM_MENU.open_multiplayer_editor_func()
                        self.MULTI_EDITOR.is_redactor = False
                        self.MULTI_EDITOR.is_redactor_open = False
                        self.MULTI_EDITOR.stun_role_label()
                        await self.websocket.send(json.dumps({"type": "get_image"}))
                    elif data["status"] == "fail":
                        print(data["status"])

                elif data["type"] == "leave_room":
                    if data["status"] == "success":
                        await asyncio.create_task(self.ROOM_MENU.update_rooms_data())

                # -------------- MULTI-EDITOR ---------------

                elif data["type"] == "create_new_image":
                    if data["status"] == "success":
                        base64_string = data["data"]
                        image_bytes = base64.b64decode(base64_string)
                        byte_array = QByteArray(image_bytes)
                        image = QImage()
                        image.loadFromData(byte_array)
                        self.MULTI_EDITOR.canvas.load_image_from_bytes(image)
                    elif data["status"] == "fail":
                        print(data["status"])

                elif data["type"] == "get_image":
                    if data["status"] == "success":
                        if data["data"] is not None:
                            base64_string = data["data"]
                            image_bytes = base64.b64decode(base64_string)
                            byte_array = QByteArray(image_bytes)
                            image = QImage()
                            image.loadFromData(byte_array)
                            self.MULTI_EDITOR.canvas.load_image_from_bytes(image)
                        else:
                            self.MULTI_EDITOR.canvas.set_new_image(16, 16)
                    elif data["status"] == "fail":
                        print(data["status"])

                elif data["type"] == "take_redactor_role":
                    if data["status"] == "success":
                        self.MULTI_EDITOR.is_redactor_open = False
                        if data["detail"] == "redactor":
                            self.MULTI_EDITOR.is_redactor = True
                            self.MULTI_EDITOR.update_role_label()
                            self.ROOM_MENU.handle_result(f"Внимание|Вы заняли роль редактора")
                        else:
                            self.MULTI_EDITOR.is_redactor = False
                            self.MULTI_EDITOR.update_role_label()
                            self.ROOM_MENU.handle_result(f"Внимание|Роль редактора была занята")
                    elif data["status"] == "fail":
                        self.ROOM_MENU.handle_result(f"Ошибка|Не удалось занять роль редактора:\n{data['detail']}")

                elif data["type"] == "leave_redactor_role":
                    if data["status"] == "success":
                        self.MULTI_EDITOR.is_redactor_open = True
                        self.MULTI_EDITOR.is_redactor = False
                        self.MULTI_EDITOR.update_role_label()
                        self.ROOM_MENU.handle_result(f"Внимание|Роль редактора освобождена")
                    elif data["status"] == "fail":
                        self.ROOM_MENU.handle_result(f"Ошибка|Не удалось снять роль редактора:\n{data['detail']}")

            except Exception as e:
                self.ROOM_MENU.handle_result(f"Ошибка|Ошибка при обработки ответа от сервера: {str(e)}")