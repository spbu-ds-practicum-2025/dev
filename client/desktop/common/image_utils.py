from PIL import Image
import base64
from io import BytesIO

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def base64_to_image(base64_str, output_path):
    img_data = base64.b64decode(base64_str)
    with open(output_path, "wb") as out_file:
        out_file.write(img_data)
