
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

INPUT_PATH = "Practical_06_Watermark_Detection_and_Analysis/input/original.png"
OUTPUT_DIR = "Practical_06_Watermark_Detection_and_Analysis/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# 1. LOAD ORIGINAL IMAGE
# --------------------------------------------------

original = Image.open(INPUT_PATH).convert("RGB")
original_array = np.array(original, dtype=np.uint8)

# --------------------------------------------------
# 2. EMBED WATERMARK USING LSB
# --------------------------------------------------

watermark_text = "NSUT WATERMARK"

# Convert text into binary
binary_watermark = ''.join(
    format(byte, '08b')
    for byte in watermark_text.encode("utf-8")
)

# Add an 8-bit end marker
binary_watermark += "11111111"

watermarked_array = original_array.copy()
flat_image = watermarked_array.reshape(-1)

# Check image capacity
if len(binary_watermark) > len(flat_image):
    raise ValueError("Image is too small to hold the watermark.")

# Embed one bit per color channel
for i, bit in enumerate(binary_watermark):
    flat_image[i] = (int(flat_image[i]) & 254) | int(bit)

watermarked_array = flat_image.reshape(original_array.shape)

Image.fromarray(watermarked_array).save(
    f"{OUTPUT_DIR}/watermarked.png"
)

# --------------------------------------------------
# 3. EXTRACT WATERMARK
# --------------------------------------------------

def extract_watermark(image):
    flat = image.reshape(-1)
    extracted_bits = []

    for value in flat:
        bit = int(value) & 1
        extracted_bits.append(str(bit))

        # Stop when the end marker is found
        if len(extracted_bits) >= 8 and ''.join(extracted_bits[-8:]) == "11111111":
            break

    bits = ''.join(extracted_bits)

    # Remove end marker
    bits = bits[:-8]

    # Convert binary into bytes
    extracted_bytes = bytearray()

    for i in range(0, len(bits) - 7, 8):
        extracted_bytes.append(int(bits[i:i+8], 2))

    try:
        return extracted_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return "Watermark could not be decoded."


extracted_watermark = extract_watermark(watermarked_array)

# --------------------------------------------------
# 4. CALCULATE MSE
# --------------------------------------------------

original_float = original_array.astype(np.float64)
watermarked_float = watermarked_array.astype(np.float64)

mse = np.mean((original_float - watermarked_float) ** 2)

# --------------------------------------------------
# 5. CALCULATE PSNR
# --------------------------------------------------

if mse == 0:
    psnr = float("inf")
else:
    psnr = 10 * np.log10((255 ** 2) / mse)

# --------------------------------------------------
# 6. CALCULATE SNR
# --------------------------------------------------

signal_power = np.sum(original_float ** 2)
noise_power = np.sum((original_float - watermarked_float) ** 2)

if noise_power == 0:
    snr = float("inf")
else:
    snr = 10 * np.log10(signal_power / noise_power)

# --------------------------------------------------
# 7. DETECT AND DISPLAY RESULTS
# --------------------------------------------------

print("\nWATERMARK DETECTION AND ANALYSIS")
print("=" * 45)

print("Original watermark :", watermark_text)
print("Extracted watermark:", extracted_watermark)

if extracted_watermark == watermark_text:
    print("Detection result   : Watermark successfully detected")
else:
    print("Detection result   : Watermark detection failed")

print("\nIMAGE QUALITY ANALYSIS")
print("=" * 45)

print(f"MSE  : {mse:.6f}")
print(f"PSNR : {psnr:.2f} dB")
print(f"SNR  : {snr:.2f} dB")

# --------------------------------------------------
# 8. DISPLAY IMAGES
# --------------------------------------------------

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(original_array)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(watermarked_array)
plt.title("Watermarked Image")
plt.axis("off")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/comparison.png")
plt.show()

print("\nPractical 6 completed successfully!")
