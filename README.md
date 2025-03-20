# Image Filtering Project

## 📌 Overview

This project **converts** RGB images to grayscale by replicating the G band in B and R, and by replicating the Y band of the YIQ system in R, G, and B.

## 📂 Project Structure

```
├── main.py          # Main script to run the filtering process
├── conversion.py   # Implements conversion operations
└── image_utils.py   # Reads and writes images, provides normalization functions
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
python main.py input_image.png color_system -o output_image.png
```

- `input_image.png` → Input image.
- `color_system` → Color system name (RGB or YIQ).
- `-o output_image.png` → (Optional) Output file name.

If `-o` is not provided, the output will be saved as `input_image_filtered.png`.

## 📜 Modules Breakdown

### `main.py`

- Reads an image (RGB)
- Replicate G band in B and R
- Convert the system RGB to YIQ
- Replicate the Y band in R, G and B
- Saves the result with an appropriate name

### `conversion.py`

- Implements **replicate_g()** for replicating G band in B and R.
- Implements **replicate_y** for calculating Y band and replicating in R, G and B.

### `image_utils.py`

- Loads and saves **RGB images**.
- Provides **absolute value transformation**.
- Implements **histogram normalization**.

## ✅ Features

✔ Works with **RGB images**.
✔ Saves output images after processing.

## 🤝 Contributions

Feel free to improve the project! You can:

- Add new conversions.
- Improve optimization.
- Extend post-processing capabilities.

---

📧 **Contact:**
- Email: reuben.ramalho@academico.ufpb.br
- Email: maria.bandeira@academico.ufpb.br