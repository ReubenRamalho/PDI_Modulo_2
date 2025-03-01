# image_utils.py
"""
Module responsible for reading and writing images (R, G, B) using Pillow (PIL).
Also contains auxiliary functions for channel manipulation and normalization.
"""

from PIL import Image
import numpy as np

def load_image(path):
    """
    Reads an image from disk and returns 3 arrays (or lists) corresponding
    to the R, G, B channels, along with the dimensions (height, width).

    :param path: Path to the image file (str)
    :return: (channelR, channelG, channelB), (height, width)
    """
    img = Image.open(path).convert("RGB")  # Ensure 3 channels
    arr = np.array(img, dtype=np.float32)  # [H, W, 3]

    # Separate each channel:
    # arr[:, :, 0] => R, arr[:, :, 1] => G, arr[:, :, 2] => B
    channelR = arr[:, :, 0]
    channelG = arr[:, :, 1]
    channelB = arr[:, :, 2]

    height, width = channelR.shape
    return (channelR, channelG, channelB), (height, width)


def save_image(path, channelR, channelG, channelB):
    """
    Receives 3 matrices (R, G, B), constructs an image, and saves it to disk.

    :param path: Path to save the image
    :param channelR: 2D matrix (height x width) for the R channel
    :param channelG: 2D matrix (height x width) for the G channel
    :param channelB: 2D matrix (height x width) for the B channel
    """
    # Create a 3D array with shape (height, width, 3)
    height, width = channelR.shape
    arr = np.zeros((height, width, 3), dtype=np.uint8)

    # Copy each channel into the correct position
    arr[:, :, 0] = np.clip(channelR, 0, 255)  # R
    arr[:, :, 1] = np.clip(channelG, 0, 255)  # G
    arr[:, :, 2] = np.clip(channelB, 0, 255)  # B

    # Create a PIL image from the array and save it
    img = Image.fromarray(arr, mode="RGB")
    img.save(path)


def absolute_value(channelR, channelG, channelB):
    """
    Applies absolute value to each channel (used for Sobel filtering, for example).

    :param channelR: 2D matrix for the R channel
    :param channelG: 2D matrix for the G channel
    :param channelB: 2D matrix for the B channel
    :return: (abs_channelR, abs_channelG, abs_channelB)
    """
    return (np.abs(channelR), np.abs(channelG), np.abs(channelB))


def normalize_0_255(channelR, channelG, channelB):
    """
    Expands the histogram of each channel individually to the [0, 255] range.

    :param channelR: 2D matrix for the R channel
    :param channelG: 2D matrix for the G channel
    :param channelB: 2D matrix for the B channel
    :return: (normalized_channelR, normalized_channelG, normalized_channelB)
    """
    # Process each channel separately
    channels = [channelR, channelG, channelB]
    normalized_channels = []

    for c in channels:
        c_min = c.min()
        c_max = c.max()

        if c_max == c_min:
            # All pixels have the same value → set everything to 0 (or 255, as needed)
            c_norm = np.zeros_like(c)
        else:
            c_norm = 255.0 * ((c - c_min) / (c_max - c_min))
        normalized_channels.append(c_norm)

    return (normalized_channels[0], normalized_channels[1], normalized_channels[2])
