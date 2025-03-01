# Image Filtering Project

## 📌 Overview

This project applies **2D correlation** on RGB images using predefined filter masks. It includes support for **Sobel edge detection**, Gaussian blur, sharpening, and more. The system reads an image, applies a filter, and saves the processed output.

## 📂 Project Structure

```
├── main.py          # Main script to run the filtering process
├── correlation.py   # Implements 2D correlation operations
├── filter_utils.py  # Loads filter parameters from a file
├── image_utils.py   # Reads and writes images, provides normalization functions
└── filters/         # Sample filter files (e.g., Sobel, Gaussian, Sharpening)
```

## 🚀 How to Use

### 1️⃣ Install Dependencies

Ensure you have **Python 3.x** installed. Required libraries:

```bash
pip install numpy pillow
```

### 2️⃣ Run the Script

To apply a filter to an image:

```bash
python main.py input_image.png filter.txt -o output_image.png
```

- `input_image.png` → Input image.
- `filter.txt` → Filter configuration file.
- `-o output_image.png` → (Optional) Output file name.

If `-o` is not provided, the output will be saved as `input_image_filtered.png`.

### 3️⃣ Example Filters

Filters are stored as text files, defining a **mask matrix**, with optional parameters like `OFFSET`, `STRIDE`, and `ACTIVATION`.

#### 🔹 **Horizontal Sobel** (`horizontal_sobel.txt`)

```
3 3
-1  0  1
-2  0  2
-1  0  1
```

#### 🔹 **Gaussian Blur** (`gaussian_blur_5x5.txt`)

```
5 5
1  4  7  4  1
4 16 26 16  4
7 26 41 26  7
4 16 26 16  4
1  4  7  4  1 
```

## 📜 Modules Breakdown

### `main.py`

- Parses command-line arguments.
- Loads the image and filter.
- Applies **2D correlation** to each channel (R, G, B).
- Detects Sobel filters and applies **post-processing** (absolute value + histogram expansion).

### `correlation.py`

- Implements **correlate2d\_single\_channel()** for single-channel filtering.
- Implements **correlate2d\_rgb()** to apply filters to RGB images.

### `filter_utils.py`

- Reads filter **mask**, **offset**, **stride**, and **activation function** from a text file.

### `image_utils.py`

- Loads and saves **RGB images**.
- Provides **absolute value transformation**.
- Implements **histogram normalization**.

## ✅ Features

✔ Supports **custom filters**.
✔ Works with **RGB images**.
✔ Detects and processes **Sobel filters** automatically.
✔ Uses **stride, offset, and activation functions**.
✔ Saves output images after processing.

## 🤝 Contributions

Feel free to improve the project! You can:

- Add new filters.
- Improve optimization.
- Extend post-processing capabilities.

---

📧 **Contact:**
- Email: reuben.ramalho@academico.ufpb.br
