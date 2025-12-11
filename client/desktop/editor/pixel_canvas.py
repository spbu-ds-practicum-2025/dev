from PyQt6.QtCore import Qt, pyqtSignal, QRect, QSize
from PyQt6.QtGui import QImage, QColor, QPainter, qRgb
from PyQt6.QtWidgets import QWidget

class PixelCanvas(QWidget):
    go_to_main_menu = pyqtSignal()
    def __init__(self, img_w=32, img_h=32, scale=10, pen_color=QColor(0, 0, 0), parent=None):
        super().__init__(parent)
        self.img_w = img_w
        self.img_h = img_h
        self.scale = scale
        self.display_size_x = img_w * self.scale
        self.display_size_y = img_h * self.scale

        self.tool = "pen"
        self.pen_color = pen_color

        self.zoom = 1.0
        self.min_zoom = 0.5
        self.max_zoom = 6.0

        self.offset_x = 0
        self.offset_y = 0
        self.max_offset = 300

        self.setMouseTracking(True)
        self.drawing = False

        self.image = QImage(self.img_w, self.img_h, QImage.Format.Format_RGB32)
        self.clear_image()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def set_tool(self, tool_name):
        self.tool = tool_name

    def set_pen_color(self, color):
        self.pen_color = color
        self.update()

    # -------------------------------------------------------------
    #                     Рисование пикселей
    # -------------------------------------------------------------

    def draw_at(self, pos):
        scaled_w = self.display_size_x * self.zoom
        scaled_h = self.display_size_y * self.zoom

        target_x = (self.width() - scaled_w) // 2 + self.offset_x
        target_y = (self.height() - scaled_h) // 2 + self.offset_y

        if not (target_x <= pos.x() <= target_x + scaled_w and
                target_y <= pos.y() <= target_y + scaled_h):
            return

        rel_x = (pos.x() - target_x) / scaled_w
        rel_y = (pos.y() - target_y) / scaled_h

        img_x = int(rel_x * self.img_w)
        img_y = int(rel_y * self.img_h)

        img_x = max(0, min(self.img_w - 1, img_x))
        img_y = max(0, min(self.img_h - 1, img_y))

        self.image.setPixel(img_x, img_y, self.pen_color.rgb())
        self.update()

    # -------------------------------------------------------------
    #                     События мыши
    # -------------------------------------------------------------

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.tool == "pen":
                self.drawing = True
                self.draw_at(event.position())

    def mouseMoveEvent(self, event):
        if self.tool == "pen":
            if self.drawing:
                self.draw_at(event.position())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    # -------------------------------------------------------------
    #                     Масштаб колесиком
    # -------------------------------------------------------------

    def wheelEvent(self, event):
        delta = event.angleDelta().y()

        if delta > 0:
            self.zoom = min(self.zoom + 0.1, self.max_zoom)
        else:
            self.zoom = max(self.zoom - 0.1, self.min_zoom)

        self.update()

    # -------------------------------------------------------------
    #                 Перемещение стрелками
    # -------------------------------------------------------------

    def keyPressEvent(self, event):
        step = 12

        if event.key() == Qt.Key.Key_Left:
            self.offset_x = min(self.offset_x + step, self.max_offset)
        elif event.key() == Qt.Key.Key_Right:
            self.offset_x = max(self.offset_x - step, -self.max_offset)
        elif event.key() == Qt.Key.Key_Up:
            self.offset_y = min(self.offset_y + step, self.max_offset)
        elif event.key() == Qt.Key.Key_Down:
            self.offset_y = max(self.offset_y - step, -self.max_offset)

        self.update()

    # -------------------------------------------------------------
    #                     Отрисовка изображения
    # -------------------------------------------------------------

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.GlobalColor.lightGray)

        scaled_w = int(self.display_size_x * self.zoom)
        scaled_h = int(self.display_size_y * self.zoom)

        target_x = (self.width() - scaled_w) // 2 + self.offset_x
        target_y = (self.height() - scaled_h) // 2 + self.offset_y

        target_x = max(0, min(self.width() - scaled_w, target_x))
        target_y = max(0, min(self.height() - scaled_h, target_y))

        target = QRect(target_x, target_y, scaled_w, scaled_h)

        painter.drawImage(target, self.image)
        painter.end()

    # -------------------------------------------------------------
    #                           Другое
    # -------------------------------------------------------------

    def clear_image(self):
        white = qRgb(255, 255, 255)
        for y in range(self.img_h):
            for x in range(self.img_w):
                self.image.setPixel(x, y, white)
        self.update()

    def set_new_image(self, width, height):
        self.img_w = width
        self.img_h = height
        self.display_size_x = width * self.scale
        self.display_size_y = height * self.scale
        self.image = QImage(self.img_w, self.img_h, QImage.Format.Format_RGB32)
        self.clear_image()

    def get_image(self):
        return self.image

    def sizeHint(self):
        return QSize(self.display_size_x, self.display_size_y)