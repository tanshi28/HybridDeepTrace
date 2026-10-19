import numpy as np
from PIL import Image


def load_image(image_path):
    image = Image.open(image_path).convert("RGB")
    return np.array(image)


def normalize_image(image):
    image = image.astype(np.float32)
    return image / 255.0