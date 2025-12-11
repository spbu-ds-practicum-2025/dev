import os.path
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QMenuBar, QVBoxLayout, QPushButton, QFrame, QLabel

from editor.pixel_canvas import PixelCanvas

color1 = "#555a64"
color2 = "#444953"
color2_1 = "#444c56"
color3 = "#333842"

class SinglePlayerEditorUI(QWidget):
    buttons_palette = [
        '#ff0000', '#c80000', '#8c0000', '#430000', '#ffffff',
        '#ff5c00', '#bb4300', '#7d2d00', '#521f00', '#b3b3b3',
        '#ffc700', '#bb9200', '#836600', '#4f3e00', '#868686',
        '#47ff00', '#36c700', '#278c00', '#195700', '#5f5f5f',
        '#00ffff', '#00bfbf', '#008b8b', '#005959', '#454545',
        '#2100ff', '#1a00ca', '#110086', '#0b0055', '#272727',
        '#9e00ff', '#8000cf', '#58008f', '#360056', '#000000'
    ]

    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Простой пиксель-редактор (Qt6)")
        self.canvas = PixelCanvas(img_w=32, img_h=32, scale=10)

        self.menu_bar = QMenuBar()
        file_menu = self.menu_bar.addMenu("Файл")
        redact_menu = self.menu_bar.addMenu("Редактирование")
        exit_menu = self.menu_bar.addMenu("Выход")
        self.save_image_action = QAction("Сохранить", self)
        self.create_new_image_action = QAction("Создать новый", self)
        self.load_image_action = QAction("Загрузить", self)
        file_menu.addAction(self.save_image_action)
        file_menu.addAction(self.create_new_image_action)
        file_menu.addAction(self.load_image_action)
        self.clear_image_action = QAction("Очистить", self)
        redact_menu.addAction(self.clear_image_action)
        self.exit_action = QAction("Выйти в меню", self)
        exit_menu.addAction(self.exit_action)

        top_layout2 = QHBoxLayout()

        left_panel = QVBoxLayout()
        self.drawing_button = QPushButton("")
        self.drawing_button.setFixedSize(40, 40)
        self.drawing_button.setStyleSheet(f"background-color: {color1}; color: white;")
        left_panel.addWidget(self.drawing_button)
        for i in range(8):
            empty_button = QPushButton(f"X")
            empty_button.setFixedSize(40, 40)
            left_panel.addWidget(empty_button)
            empty_button.setStyleSheet(f"background-color: {color1}; color: white;")
        empty_line_left = QFrame()
        empty_line_left.setFrameShape(QFrame.Shape.VLine)
        empty_line_left.setFrameShadow(QFrame.Shadow.Sunken)
        left_panel.addWidget(empty_line_left)

        right_panel = QVBoxLayout()
        self.color_buttons = []
        for i in range(7):
            row_layout = QHBoxLayout()
            for j in range(5):
                c = i * 5 + j
                color_button = QPushButton()
                color_button.setFixedSize(35, 35)
                self.color_buttons.append([color_button, c])
                color_button.resize(10, 4)
                row_layout.addWidget(color_button)
            right_panel.addLayout(row_layout)
        empty_line_right = QFrame()
        empty_line_right.setFrameShape(QFrame.Shape.VLine)
        empty_line_right.setFrameShadow(QFrame.Shadow.Sunken)
        right_panel.addWidget(empty_line_right)

        top_layout1 = QHBoxLayout()
        top_layout1.setContentsMargins(0, 0, 0, 0)
        top_layout1.addWidget(self.menu_bar)
        top_frame1 = QFrame()
        top_frame1.setLayout(top_layout1)
        top_frame1.setMaximumHeight(25)
        top_frame2 = QFrame()
        top_frame2.setLayout(top_layout2)
        top_frame2.setMaximumHeight(60)
        central_frame = QHBoxLayout()
        central_frame.addLayout(left_panel)
        central_frame.addWidget(self.canvas)
        central_frame.addLayout(right_panel)
        self.tool_info_label = QLabel()
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.tool_info_label)
        bottom_frame = QFrame()
        bottom_frame.setLayout(bottom_layout)
        bottom_frame.setMaximumHeight(30)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(top_frame1)
        main_layout.addWidget(top_frame2)
        main_layout.addLayout(central_frame)
        main_layout.addWidget(bottom_frame)
        self.setLayout(main_layout)

        top_frame1.setStyleSheet(f"background-color: {color1}; border: none;")
        self.menu_bar.setStyleSheet("color: white;")
        file_menu.setStyleSheet("color: white;")
        exit_menu.setStyleSheet("color: white;")
        redact_menu.setStyleSheet("color: white;")
        top_frame2.setStyleSheet(f"background-color: {color2}; border: none;")
        bottom_frame.setStyleSheet(f"background-color: {color2}; color: white;")
        self.setStyleSheet(f"background-color: {color3}; color: white;")
        for color_button, color_id in self.color_buttons:
            color_button.setStyleSheet(f"background-color: {SinglePlayerEditorUI.buttons_palette[color_id]};")
        self.drawing_button.setIcon(QIcon(os.path.join("assets", 'icons', 'pencil.png')))
        self.drawing_button.setIconSize(QSize(32, 32))
