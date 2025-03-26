# correlation.py
"""
Module that implements:
- 2D correlation (without padding)
- Version with offset, stride, and ReLU (item 2)
- Function to apply correlation to all channels (R, G, B)
"""

import numpy as np

def correlate2d_single_channel(
    channel, mask, offset=0, stride=1, activation=None
):
    """
    Applies 2D correlation to a single channel (2D matrix),
    without border extension.

    :param channel: np.array 2D representing the input channel
    :param mask: 2D list (or np.array 2D) representing the mask
    :param offset: integer to be added after summing (bias)
    :param stride: step size (integer > 0)
    :param activation: if "RELU", applies ReLU after adding offset
    :return: np.array 2D with the correlation result
    """
    m = len(mask)       # Number of rows in the mask
    n = len(mask[0])    # Number of columns in the mask

    H, W = channel.shape
    # Output size considering stride and no padding
    out_height = (H - m) // stride + 1
    out_width  = (W - n) // stride + 1

    # Convert mask to np.array (optional)
    mask_np = np.array(mask, dtype=np.int32)

    # Create output array
    output = np.zeros((out_height, out_width), dtype=np.int32)

    # Loop over the image (without padding)
    out_i = 0
    for i in range(0, H - m + 1, stride):
        out_j = 0
        for j in range(0, W - n + 1, stride):

            # Extract the corresponding region (m x n)
            region = channel[i : i+m, j : j+n]

            # Sum of element-wise multiplication
            # Note: Correlation and convolution differ in mask flipping,
            # but we assume it is "correlation" without flipping.
            # If convolution were needed, we would invert the mask.
            value = np.sum(region * mask_np)

            # Apply offset if provided (item 2)
            value += offset

            # Apply activation function (ReLU) if necessary
            if activation == "RELU":
                value = max(0, value)

            output[out_i, out_j] = value
            out_j += 1
        out_i += 1

    return output


def correlate2d_rgb(
    channelR, channelG, channelB,
    mask, offset=0, stride=1, activation=None
):
    """
    Applies correlate2d_single_channel to each channel separately.
    Returns R, G, B results.
    """
    outR = correlate2d_single_channel(
        channelR, mask, offset=offset, stride=stride, activation=activation
    )
    outG = correlate2d_single_channel(
        channelG, mask, offset=offset, stride=stride, activation=activation
    )
    outB = correlate2d_single_channel(
        channelB, mask, offset=offset, stride=stride, activation=activation
    )
    return outR, outG, outB
