# filter_utils.py
"""
Module responsible for reading filter parameters:
- Dimensions (m, n)
- Mask values (matrix)
- (Optional) Offset, Stride, and Activation Type
"""

def load_filter_from_file(path):
    """
    Reads a filter file and returns a dictionary containing:
    - Filter dimensions (m, n)
    - Filter matrix (mask)
    - Offset (optional)
    - Stride (optional, default = 1)
    - Activation function (optional)

    Example filter file:
    ------------------------------
    5 5
    1 2 3 2 1
    2 4 6 4 2
    3 6 9 6 3
    2 4 6 4 2
    1 2 3 2 1
    OFFSET 10
    STRIDE 2
    ACTIVATION RELU
    ------------------------------
    """

    with open(path, "r") as f:
        # Read all lines from the file, removing extra spaces and empty lines
        lines = [line.strip() for line in f if line.strip()]

    # --- 1. Extract filter dimensions ---
    first_line = lines[0].split()  # First line contains "m n"
    m = int(first_line[0])  # Number of rows in the mask
    n = int(first_line[1])  # Number of columns in the mask

    # --- 2. Read mask values ---
    mask = []
    line_index = 1  # Current line index in the file (starting after dimensions)

    for i in range(m):  # We need to read 'm' lines to construct the filter matrix
        values = lines[line_index].split()  # Split numbers into a list
        line_index += 1  # Move to the next line
        row = [float(v) for v in values]  # Convert each value to float
        mask.append(row)  # Add the row to the mask matrix

    # --- 3. Initialize optional parameters ---
    offset = None
    stride = 1  # Default value
    activation = None

    # --- 4. Read optional parameters (OFFSET, STRIDE, ACTIVATION) ---
    while line_index < len(lines):  # Continue reading until end of file
        line = lines[line_index]
        line_index += 1
        parts = line.split()

        if len(parts) >= 2:
            key = parts[0].upper()  # Key (e.g., "OFFSET", "STRIDE", "ACTIVATION")
            value = parts[1].upper() if len(parts) == 2 else parts[1:]

            if key == "OFFSET":
                offset = int(parts[1])  # Convert to integer

            elif key == "STRIDE":
                stride = int(parts[1])  # Convert to integer

            elif key == "ACTIVATION":
                activation = value  # Store the string (e.g., "RELU")

    # --- 5. Return extracted data ---
    return {
        "m": m,
        "n": n,
        "mask": mask,
        "offset": offset,
        "stride": stride,
        "activation": activation
    }
