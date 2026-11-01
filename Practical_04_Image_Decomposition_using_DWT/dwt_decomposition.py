
import os
import numpy as np
import pywt
import importlib
from PIL import Image

# Define paths
input_path = "Practical_04_Image_Decomposition_using_DWT/input/original.png"
output_dir = "Practical_04_Image_Decomposition_using_DWT/output"

os.makedirs(output_dir, exist_ok=True)

# Load image and convert to grayscale
image = Image.open(input_path).convert("L")
image_array = np.array(image)

# Apply 2D Haar Discrete Wavelet Transform
LL, (LH, HL, HH) = pywt.dwt2(image_array, "haar")

# Normalize detail coefficients for visualization
def normalize_band(band):
    band = np.abs(band)
    band = (band - band.min()) / (band.max() - band.min() + 1e-10)
    return (band * 255).astype(np.uint8)

# Convert approximation and detail bands for display
LL_display = normalize_band(LL)
LH_display = normalize_band(LH)
HL_display = normalize_band(HL)
HH_display = normalize_band(HH)

# Save all four subbands
Image.fromarray(LL_display).save(f"{output_dir}/LL_approximation.png")
Image.fromarray(LH_display).save(f"{output_dir}/LH_horizontal_detail.png")
Image.fromarray(HL_display).save(f"{output_dir}/HL_vertical_detail.png")
Image.fromarray(HH_display).save(f"{output_dir}/HH_diagonal_detail.png")

# Display decomposition when Matplotlib is available.
try:
    plt = importlib.import_module("matplotlib.pyplot")
except ImportError:
    plt = None

if plt is not None:
    plt.figure(figsize=(12, 8))

    bands = [
        (LL_display, "LL - Approximation"),
        (LH_display, "LH - Horizontal Detail"),
        (HL_display, "HL - Vertical Detail"),
        (HH_display, "HH - Diagonal Detail")
    ]

    for i, (band, title) in enumerate(bands):
        plt.subplot(2, 2, i + 1)
        plt.imshow(band, cmap="gray")
        plt.title(title)
        plt.axis("off")

    plt.tight_layout()
    plt.savefig(f"{output_dir}/dwt_decomposition.png")
    plt.show()

print("DWT decomposition completed successfully!")
print("Original image shape:", image_array.shape)
print("LL shape:", LL.shape)
print("LH shape:", LH.shape)
print("HL shape:", HL.shape)
print("HH shape:", HH.shape)
