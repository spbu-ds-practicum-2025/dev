import io
import base64
from PIL import Image

class ProcessingServerService:
    def __init__(self):
        self.image = None

    def set_image(self, base64_str):
        img_data = base64.b64decode(base64_str)
        img_io = io.BytesIO(img_data)
        self.image = Image.open(img_io)

    def create_new_image(self, height, width):
        self.image = Image.new('RGB', (height, width), color=(255, 255, 255))

    def return_image_json(self):
        if self.image is None:
            return None

        buffer = io.BytesIO()
        self.image.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return {"data": img_str}
