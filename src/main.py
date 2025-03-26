# main.py
"""
Main script that:
1) Reads an image (RGB).
2) Reads filter parameters from an external file.
3) Applies 2D correlation to the image.
4) Saves the R, G, B result matrices to a .txt file (human-readable).
5) If the filter is Sobel, applies detection (absolute value + histogram expansion).
6) Displays the final image on screen.
"""

import os
import argparse
import numpy as np
import matplotlib.pyplot as plt

from image_utils import load_image, absolute_value, normalize_0_255
from filter_utils import load_filter_from_file
from correlation import correlate2d_rgb

def resolve_path(path):
    """
    Converts a relative path to an absolute path.
    If the path is already absolute, it remains unchanged.
    """
    return os.path.abspath(path)

def is_sobel_filter(mask):
    """
    Checks if a filter is Sobel (horizontal or vertical) for any size.

    Horizontal Sobel: negative on the top rows, positive on the bottom rows.
    Vertical Sobel:  negative on the left columns, positive on the right columns.
    """
    m, n = len(mask), len(mask[0])

    # Check horizontal pattern (top negative, bottom positive)
    is_horizontal = True
    for i in range(m):
        for j in range(n):
            if i < (m // 2) and mask[i][j] >= 0:
                is_horizontal = False
            elif i > (m // 2) and mask[i][j] <= 0:
                is_horizontal = False

    # Check vertical pattern (left negative, right positive)
    is_vertical = True
    for i in range(m):
        for j in range(n):
            if j < (n // 2) and mask[i][j] >= 0:
                is_vertical = False
            elif j > (n // 2) and mask[i][j] <= 0:
                is_vertical = False

    return is_horizontal or is_vertical

def parse_args():
    """
    Configures and interprets command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Applies a convolution filter to an RGB image, saves the R/G/B matrices to a .txt file, and optionally does Sobel detection."
    )

    parser.add_argument("input_image", type=str, help="Path to the input image.")
    parser.add_argument("filter", type=str, help="Path to the filter file.")
    parser.add_argument(
        "-o", "--output", type=str, default=None,
        help=(
            "Path to save the R, G, B matrices in a text file. "
            "If no extension is given, '.txt' is appended. "
            "If not provided at all, defaults to '<inputname>_filtered.txt'."
        )
    )

    return parser.parse_args()

def save_rgb_to_txt(path, outR, outG, outB):
    """
    Saves the R, G, B matrices into a single text file in a human-readable format.

    :param path: Where to save the .txt file
    :param outR, outG, outB: np.array 2D for each channel
    """
    with open(path, "w", encoding="utf-8") as f:
        # Save shape info
        f.write("# R, G, B channel matrices\n")
        f.write(f"# Dimensions (R): {outR.shape[0]} x {outR.shape[1]}\n")
        f.write(f"# Dimensions (G): {outG.shape[0]} x {outG.shape[1]}\n")
        f.write(f"# Dimensions (B): {outB.shape[0]} x {outB.shape[1]}\n\n")

        # Write R channel
        f.write("=== Matrix R ===\n")
        for row in outR:
            row_str = " ".join(f"{val}" for val in row)
            f.write(row_str + "\n")
        f.write("\n")

        # Write G channel
        f.write("=== Matrix G ===\n")
        for row in outG:
            row_str = " ".join(f"{val}" for val in row)
            f.write(row_str + "\n")
        f.write("\n")

        # Write B channel
        f.write("=== Matrix B ===\n")
        for row in outB:
            row_str = " ".join(f"{val}" for val in row)
            f.write(row_str + "\n")

def main():
    # 1. Parse command line arguments
    args = parse_args()

    input_image_path = resolve_path(args.input_image)
    filter_path = resolve_path(args.filter)

    # Determine text file path for saving R, G, B
    if args.output:
        matrix_save_path = resolve_path(args.output)
        if not os.path.splitext(matrix_save_path)[1]:
            matrix_save_path += ".txt"
    else:
        base_name, _ = os.path.splitext(input_image_path)
        matrix_save_path = f"{base_name}_filtered.txt"

    # 2. Load the image (R, G, B)
    (R, G, B), (H, W) = load_image(input_image_path)
    print(f"Image loaded: {input_image_path} ({H}x{W})")

    # 3. Load filter parameters
    filter_info = load_filter_from_file(filter_path)
    m = filter_info["m"]
    n = filter_info["n"]
    mask = filter_info["mask"]
    offset = filter_info["offset"] if filter_info["offset"] is not None else 0
    stride = filter_info["stride"] if filter_info["stride"] else 1
    activation = filter_info["activation"] if filter_info["activation"] else None

    print("Filter successfully loaded:")
    print(f"Dimensions: {m}x{n}")
    for row in mask:
        print(row)
    print(f"Offset: {offset}")
    print(f"Stride: {stride}")
    print(f"Activation: {activation}")

    # 4. Apply 2D correlation
    outR, outG, outB = correlate2d_rgb(
        R, G, B,
        mask=mask,
        offset=offset,
        stride=stride,
        activation=activation
    )

    # Save the intermediate R, G, B matrices to a text file
    print(f"Saving R, G, B matrices to: {matrix_save_path}")
    save_rgb_to_txt(matrix_save_path, outR, outG, outB)

    # 5. If the filter is Sobel, do absolute value + normalization
    if is_sobel_filter(mask):
        print("Sobel filter detected. Applying post-processing...")
        outR, outG, outB = absolute_value(outR, outG, outB)
        outR, outG, outB = normalize_0_255(outR, outG, outB)

    # 6. Display final image
    print("Displaying final image result...")
    final_image = np.stack([
        np.clip(outR, 0, 255),
        np.clip(outG, 0, 255),
        np.clip(outB, 0, 255)
    ], axis=-1).astype(np.uint8)

    plt.imshow(final_image)
    plt.title("Filtered Image")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()
