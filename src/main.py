# main.py
"""
Main script that:
1) Reads an image (RGB)
2) Reads filter parameters from an external file
3) Applies 2D correlation to the image
4) Automatically detects if the filter is Sobel (horizontal or vertical) of any size
5) If it is Sobel, applies absolute value + histogram expansion
6) Saves the result with an appropriate name
"""

import os
import argparse
import numpy as np
from image_utils import load_image, save_image, absolute_value, normalize_0_255
from filter_utils import load_filter_from_file
from correlation import correlate2d_rgb

def resolve_path(path):
    """
    Resolves the given path to an absolute path.
    If the path is already absolute, it remains unchanged.
    
    :param path: The file path to resolve
    :return: Absolute path
    """
    return os.path.abspath(path)

def is_sobel_filter(mask):
    """
    Detects if a filter is Sobel (horizontal or vertical) for any size.

    - Horizontal Sobel: values increase from top to bottom.
    - Vertical Sobel: values increase from left to right.

    :param mask: Filter matrix
    :return: True if it is Sobel, False otherwise
    """
    m, n = len(mask), len(mask[0])  # Filter dimensions

    # Check if it is Horizontal Sobel (values increase from top to bottom)
    is_horizontal = True
    for i in range(m):
        for j in range(n):
            if i < m // 2 and mask[i][j] >= 0:  # Top should be negative
                is_horizontal = False
            elif i > m // 2 and mask[i][j] <= 0:  # Bottom should be positive
                is_horizontal = False
                
    # Check if it is Vertical Sobel (values increase from left to right)
    is_vertical = True
    for i in range(m):
        for j in range(n):
            if j < n // 2 and mask[i][j] >= 0:  # Left side should be negative
                is_vertical = False
            elif j > n // 2 and mask[i][j] <= 0:  # Right side should be positive
                is_vertical = False

    return is_horizontal or is_vertical  # Returns True if it is any Sobel

def parse_args():
    """
    Configures and interprets command-line arguments.

    :return: Program arguments
    """
    parser = argparse.ArgumentParser(description="Applies a convolution filter to an RGB image.")
    
    parser.add_argument("input_image", type=str, help="Path to the input image.")
    parser.add_argument("filter", type=str, help="Path to the filter file.")
    parser.add_argument(
        "-o", "--output", type=str, default=None,
        help="Path to save the filtered image. If no extension is provided, the image is saved as PNG by default.")

    return parser.parse_args()


def main():
    # ========== 1. PARSE ARGUMENTS ===========
    args = parse_args()
    
    # Resolve absolute paths for input image and filter
    input_image_path = resolve_path(args.input_image)
    filter_path = resolve_path(args.filter)

    # If no output path is provided, create an automatic name
    if args.output:
        output_image_path = resolve_path(args.output)
        # Ensure the output file has an extension
        if not os.path.splitext(output_image_path)[1]:  
            output_image_path += ".png"  # Default to PNG
    else:
        base_name, extension = os.path.splitext(input_image_path)
        output_image_path = f"{base_name}_filtered{extension}"

    # ========== 2. READ IMAGE ===========
    (R, G, B), (H, W) = load_image(input_image_path)
    print(f"Image loaded: {input_image_path} ({H}x{W})")

    # ========== 3. READ FILTER ===========
    filter_info = load_filter_from_file(filter_path)
    m = filter_info["m"]
    n = filter_info["n"]
    mask = filter_info["mask"]
    offset = filter_info["offset"] if filter_info["offset"] is not None else 0
    stride = filter_info["stride"] if filter_info["stride"] else 1
    activation = filter_info["activation"] if filter_info["activation"] else None

    print("Filter successfully loaded:")
    print(f"Dimensions: {m}x{n}")
    print("Mask:")
    for row in mask:
        print(row)
    print(f"Offset: {offset}")
    print(f"Stride: {stride}")
    print(f"Activation: {activation}")

    # ========== 4. APPLY 2D CORRELATION ===========
    outR, outG, outB = correlate2d_rgb(
        R, G, B,
        mask=mask,
        offset=offset,
        stride=stride,
        activation=activation
    )

    # ========== 5. DETECT SOBEL FILTER ===========
    if is_sobel_filter(mask):
        print("Filter detected as Sobel (horizontal or vertical). Applying post-processing...")
        
        # 5.1 Apply absolute value (|x|)
        outR, outG, outB = absolute_value(outR, outG, outB)

        # 5.2 Expand histogram to [0,255]
        outR, outG, outB = normalize_0_255(outR, outG, outB)

    # ========== 6. SAVE RESULT ===========
    save_image(output_image_path, outR, outG, outB)
    print(f"Filtered image saved at: {output_image_path}")

if __name__ == "__main__":
    main()
