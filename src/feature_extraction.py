import cv2
import numpy as np

from PIL import Image
from skimage.feature import local_binary_pattern


def extract_texture_features(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    lbp = local_binary_pattern(
        gray,
        P=8,
        R=1,
        method="uniform"
    )

    histogram, _ = np.histogram(
        lbp,
        bins=np.arange(0, 11),
        range=(0, 10)
    )

    histogram = histogram.astype(np.float32)
    histogram /= histogram.sum() + 1e-7

    return histogram


def extract_frequency_features(image):
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2GRAY
    )

    gray = np.float32(gray)

    dct = cv2.dct(gray)

    low_frequency = np.mean(
        np.abs(dct[:8, :8])
    )

    high_frequency = np.mean(
        np.abs(dct[8:, 8:])
    )

    return np.array([
        low_frequency,
        high_frequency
    ])


def extract_statistics(image):
    features = []

    for channel in range(3):
        channel_data = image[:, :, channel]

        features.extend([
            np.mean(channel_data),
            np.std(channel_data),
            np.min(channel_data),
            np.max(channel_data)
        ])

    return np.array(features, dtype=np.float32)


def extract_features(image_path):
    image = Image.open(image_path).convert("RGB")
    image = np.array(image)

    texture_features = extract_texture_features(image)

    frequency_features = extract_frequency_features(image)

    statistical_features = extract_statistics(image)

    features = np.concatenate([
        texture_features,
        frequency_features,
        statistical_features
    ])

    return features