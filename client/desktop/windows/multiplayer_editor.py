import asyncio
import base64
import types
import json
from websockets.protocol import State

from PyQt6.QtCore import Qt, QByteArray, QBuffer, QIODevice
from PyQt6.QtWidgets import QFileDialog, QDialog, QMessageBox
from qasync import asyncSlot

from utils.client_websocket import ClientWebSocket
from ui.multiplayer_editor_ui import MultiPlayerEditorUI
from .resize_dialog import ResizeDialog

class MultiPlayerEditorWindow(MultiPlayerEditorUI):
    def __init__(self, parent, client_websocket: ClientWebSocket):
        super().__init__(parent)
        self.CW = client_websocket
        self.is_redactor = False
        self.is_redactor_open = False

        def newMouseReleaseEvent(self, event, editor=self):
            if event.button() == Qt.MouseButton.LeftButton:
                self.drawing = False

                image = self.get_image()
                ba = QByteArray()
                buffer = QBuffer(ba)
                buffer.open(QIODevice.OpenModeFlag.WriteOnly)
                image.save(buffer, "PNG")
                raw_bytes = ba.data()
                base64_str = base64.b64encode(raw_bytes).decode('utf-8')

                editor.send_current_image_to_server(base64_str)

        def new_set_pixel(self, x, y, color, editor=self):
            if editor.is_redactor:
                self.image.setPixel(x, y, color)
                self.update()

        self.canvas.mouseReleaseEvent = types.MethodType(newMouseReleaseEvent, self.canvas)
        self.canvas.set_pixel = types.MethodType(new_set_pixel, self.canvas)


        self.save_image_action.triggered.connect(self.save_image)
        self.create_new_image_action.triggered.connect(self.create_new_image)
        self.clear_image_action.triggered.connect(self.clear_image)
        self.exit_action.triggered.connect(self.exit_to_menu)

        self.btn_take_role.clicked.connect(self.take_redactor_role)
        self.btn_leave_role.clicked.connect(self.leave_redactor_role)
        self.drawing_button.clicked.connect(lambda: self.select_tool("pen"))

        for color_button, color_id in self.color_buttons:
            color_button.clicked.connect(lambda _, x=color_id: self.change_color(x))

        self.update_info_label()


    @asyncSlot()
    async def clear_image(self):
        if not self.is_redactor:
            self.handle_result(f"Ошибка|Невозможно отчистить изображение - вы не являетесь редатором!")
            return

        width, height = self.canvas.img_w, self.canvas.img_h
        await self.CW.websocket.send(json.dumps({"type": "create_new_image", "height": height, "width": width}))

    @asyncSlot()
    async def create_new_image(self):
        if not self.is_redactor:
            self.handle_result(f"Ошибка|Невозможно создать изображение - вы не являетесь редатором!")
            return

        dialog = ResizeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            width, height = dialog.get_input()
            await self.CW.websocket.send(json.dumps({"type": "create_new_image", "height": height, "width": width}))

    @asyncSlot()
    async def send_current_image_to_server(self, img_str):
        if not self.is_redactor:
            self.handle_result(f"Ошибка|Невозможно изменять изображение - вы не являетесь редатором!")
            return

        width, height = self.canvas.img_w, self.canvas.img_h
        await self.CW.websocket.send(json.dumps({"type": "send_image", "height": height, "width": width, "img_str": img_str}))


    @asyncSlot()
    async def exit_to_menu(self):
        self.canvas.go_to_main_menu.emit()

        if self.CW.websocket and self.CW.websocket.state == State.OPEN:
            try:
                await self.CW.websocket.send(json.dumps({"type": "leave_room"}))
                await self.CW.websocket.send(json.dumps({"type": "get_info"}))
            except asyncio.TimeoutError:
                self.handle_result("Ошибка|Ошибка при выходе из комнат:\nТаймаут при ожидании ответа.")
            except Exception as e:
                self.handle_result(f"Ошибка|Ошибка при выходе из комнаты: {str(e)}")

    def save_image(self):
        qimg = self.canvas.get_image()
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "", "PNG Files (*.png)")
        if filename:
            if not filename.lower().endswith(".png"):
                filename += ".png"
            qimg.save(filename, "PNG")

    @asyncSlot()
    async def take_redactor_role(self):
        if self.CW.websocket and self.CW.websocket.state == State.OPEN:
            try:
                await self.CW.websocket.send(json.dumps({"type": "take_redactor_role"}))
            except Exception as e:
                self.handle_result(f"Ошибка|Ошибка при взятии роли редактора: {str(e)}")

    @asyncSlot()
    async def leave_redactor_role(self):
        if self.CW.websocket and self.CW.websocket.state == State.OPEN:
            try:
                await self.CW.websocket.send(json.dumps({"type": "leave_redactor_role"}))
            except Exception as e:
                self.handle_result(f"Ошибка|Ошибка при взятии роли редактора: {str(e)}")

    def handle_result(self, result):
        title, message = result.split('|')
        QMessageBox.information(self, title, message)

    def update_role_label(self):
        if self.is_redactor:
            self.role_status_label.setText("  Роль редактора: <span style='color: #10b02b;'>занята вами.</span>")
        elif not self.is_redactor and not self.is_redactor_open:
            self.role_status_label.setText("  Роль редактора: <span style='color: #dbb700;'>занята не вами.</span>")
        elif not self.is_redactor and self.is_redactor_open:
            self.role_status_label.setText("  Роль редактора: <span style='color: #13a6cf;'>свободна.</span>")

    def stun_role_label(self):
        self.role_status_label.setText("  Роль редактора: <Ожидание>")
