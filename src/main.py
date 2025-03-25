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
from PIL import Image
from filter_utils import load_3d_filter_from_file
from image_utils import abs_and_expand_hist
from correlation import corretlated_3d_mask

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
    m, n, c = len(mask), len(mask[0]), len(mask[0][0])  # Filter dimensions

    # Check if it is Horizontal Sobel (values increase from top to bottom)
    is_horizontal = True
    for i in range(m):
        for j in range(n):
            for k in range(c):
                if i < m // 2 and mask[i][j][k] >= 0:  # Top should be negative
                    is_horizontal = False
                elif i > m // 2 and mask[i][j][k] <= 0:  # Bottom should be positive
                    is_horizontal = False
                
    # Check if it is Vertical Sobel (values increase from left to right)
    is_vertical = True
    for i in range(m):
        for j in range(n):
            for k in range(c):
                if j < n // 2 and mask[i][j][k] >= 0:  # Left side should be negative
                    is_vertical = False
                elif j > n // 2 and mask[i][j][k] <= 0:  # Right side should be positive
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
    image = Image.open(input_image_path)
    print(f"Image loaded: {input_image_path} ({image.size[1]}x{image.size[0]})")

    # ========== 3. READ FILTER ===========
    mask = load_3d_filter_from_file(filter_path)

    # ========== 4. APPLY 2D CORRELATION ===========
    out = corretlated_3d_mask(mask, image)

    # ========== 5. DETECT SOBEL FILTER ===========
    if is_sobel_filter(mask):
        print("Filter detected as Sobel (horizontal or vertical). Applying post-processing...")
        
        out = abs_and_expand_hist(out)
    
    else:
        out = out.astype(np.uint8)

    # ========== 6. SAVE RESULT ===========
    Image.fromarray(out).save(output_image_path, "PNG")
    print(f"Filtered image saved at: {output_image_path}")

if __name__ == "__main__":
    main()