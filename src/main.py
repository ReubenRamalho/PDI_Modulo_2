# main.py
"""
Main script that:
1) Reads an image (RGB)
2) Replicate G band in B and R
3) Convert the system RGB to YIQ
4) Replicate the Y band in R, G and B
5) Saves the result with an appropriate name
"""

import os
import argparse
import numpy as np
from image_utils import load_image, save_image, absolute_value, normalize_0_255
from conversion import replicate_g, replicate_y

def resolve_path(path):
    """
    Resolves the given path to an absolute path.
    If the path is already absolute, it remains unchanged.
    
    :param path: The file path to resolve
    :return: Absolute path
    """
    return os.path.abspath(path)

def parse_args():
    """
    Configures and interprets command-line arguments.

    :return: Program arguments
    """
    parser = argparse.ArgumentParser(description="Convert a RGB image to grayscale.")
    
    parser.add_argument("input_image", type=str, help="Path to the input image.")
    parser.add_argument("conversion", type=str, help="Name of the system used to convert image (RGB or YIQ).")
    parser.add_argument(
        "-o", "--output", type=str, default=None,
        help="Path to save the converted image. If no extension is provided, the image is saved as PNG by default.")

    return parser.parse_args()


def main():
    # ========== 1. PARSE ARGUMENTS ===========
    args = parse_args()
    
    # Resolve absolute paths for input image and filter
    input_image_path = resolve_path(args.input_image)
    color_system = args.conversion

    # If no output path is provided, create an automatic name
    if args.output:
        output_image_path = resolve_path(args.output)
        # Ensure the output file has an extension
        if not os.path.splitext(output_image_path)[1]:  
            output_image_path += ".png"  # Default to PNG
    else:
        base_name, extension = os.path.splitext(input_image_path)
        output_image_path = f"{base_name}_grayscale{extension}"

    # ========== 2. READ IMAGE ===========
    (R, G, B), (H, W) = load_image(input_image_path)
    print(f"Image loaded: {input_image_path} ({H}x{W})")

    # ========== 3. APPLY CONVERSION ===========
    
    if color_system == 'RGB':
        outR, outG, outB = replicate_g(
        R, G, B
    )
    
    elif color_system == 'YIQ':
        outR, outG, outB = replicate_y(
        R, G, B
    )
    
    # ========== 6. SAVE RESULT ===========
    save_image(output_image_path, outR, outG, outB)
    print(f"Converted image to grayscale saved at: {output_image_path}")

if __name__ == "__main__":
    main()
