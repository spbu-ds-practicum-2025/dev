from PyQt6.QtGui import QImage, QColor
from PyQt6.QtWidgets import QFileDialog, QDialog

from ui.singleplayer_editor_ui import SinglePlayerEditorUI
from .resize_dialog import ResizeDialog

class EditorWindow(SinglePlayerEditorUI):
    def __init__(self, parent):
        super().__init__(parent)

        self.save_image_action.triggered.connect(self.save_image)
        self.create_new_image_action.triggered.connect(self.create_new_image)
        self.load_image_action.triggered.connect(self.load_image)
        self.clear_image_action.triggered.connect(self.clear_image)
        self.exit_action.triggered.connect(self.exit_to_menu)

        self.drawing_button.clicked.connect(lambda: self.select_tool("pen"))

        for color_button, color_id in self.color_buttons:
            color_button.clicked.connect(lambda _, x=color_id: self.change_color(x))

        self.update_info_label()

    def select_tool(self, tool_name):
        self.canvas.set_tool(tool_name)
        self.update_info_label()

    def update_info_label(self):
        tool = self.canvas.tool
        color = self.canvas.pen_color.name()
        self.tool_info_label.setText(f"Инструмент: {tool} | Цвет: {color}")

    def change_color(self, color_id):
        color = QColor(SinglePlayerEditorUI.buttons_palette[color_id])
        self.canvas.set_pen_color(color)
        self.update_info_label()

    def clear_image(self):
        self.canvas.clear_image()
        self.update_info_label()

    def save_image(self):
        qimg = self.canvas.get_image()
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "", "PNG Files (*.png)")
        if filename:
            if not filename.lower().endswith(".png"):
                filename += ".png"
            qimg.save(filename, "PNG")

    def create_new_image(self):
        dialog = ResizeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            width, height = dialog.get_input()
            self.canvas.set_new_image(width, height)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Открыть изображение", "", "PNG Files (*.png);;All Files (*)")
        if file_name:
            image = QImage(file_name)
            if image.isNull():
                print("Не удалось загрузить изображение.")
            else:
                self.canvas.set_new_image(image.width(), image.height())
                self.canvas.image = image
                self.canvas.display_size_x = image.width() * self.canvas.scale
                self.canvas.display_size_y = image.height() * self.canvas.scale

                self.canvas.update()

    def exit_to_menu(self):
        self.canvas.go_to_main_menu.emit()
