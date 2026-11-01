
import os
import numpy as np
from PIL import Image

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

INPUT_PATH = "Practical_08_Copyright_Protection/input/original.png"
OUTPUT_DIR = "Practical_08_Copyright_Protection/output"

OUTPUT_PATH = os.path.join(OUTPUT_DIR, "copyright_watermarked.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Ownership information
OWNER_INFO = "NSUT COPYRIGHT OWNER"

# --------------------------------------------------
# 1. LOAD ORIGINAL IMAGE
# --------------------------------------------------

image = Image.open(INPUT_PATH).convert("RGB")
image_array = np.array(image, dtype=np.uint8)

# --------------------------------------------------
# 2. EMBED OWNERSHIP WATERMARK
# --------------------------------------------------

def embed_watermark(image_array, message):

    binary_message = ''.join(
        format(byte, "08b")
        for byte in message.encode("utf-8")
    )

    # Add an 8-bit end marker
    binary_message += "11111111"

    flat_image = image_array.reshape(-1).copy()

    if len(binary_message) > len(flat_image):
        raise ValueError("Image does not have enough capacity.")

    for i, bit in enumerate(binary_message):
        flat_image[i] = (
            (int(flat_image[i]) & 254) | int(bit)
        )

    return flat_image.reshape(image_array.shape)


# --------------------------------------------------
# 3. EXTRACT OWNERSHIP WATERMARK
# --------------------------------------------------

def extract_watermark(image_array):

    flat_image = image_array.reshape(-1)

    extracted_bits = []

    for value in flat_image:

        bit = str(int(value) & 1)
        extracted_bits.append(bit)

        if (
            len(extracted_bits) >= 8
            and ''.join(extracted_bits[-8:]) == "11111111"
        ):
            break

    bits = ''.join(extracted_bits[:-8])

    extracted_bytes = bytearray()

    for i in range(0, len(bits) - 7, 8):
        extracted_bytes.append(int(bits[i:i+8], 2))

    return extracted_bytes.decode("utf-8")


# --------------------------------------------------
# 4. EMBEDDING
# --------------------------------------------------

watermarked_array = embed_watermark(
    image_array,
    OWNER_INFO
)

Image.fromarray(
    watermarked_array.astype(np.uint8)
).save(OUTPUT_PATH)

print("\nCOPYRIGHT WATERMARK EMBEDDING")
print("=" * 45)
print("Owner information:", OWNER_INFO)
print("Watermarked image saved:", OUTPUT_PATH)

# --------------------------------------------------
# 5. EXTRACTION
# --------------------------------------------------

saved_image = Image.open(OUTPUT_PATH).convert("RGB")
saved_array = np.array(saved_image, dtype=np.uint8)

extracted_info = extract_watermark(saved_array)

print("\nWATERMARK EXTRACTION")
print("=" * 45)
print("Extracted ownership information:", extracted_info)

# --------------------------------------------------
# 6. AUTHENTICITY VERIFICATION
# --------------------------------------------------

print("\nAUTHENTICITY VERIFICATION")
print("=" * 45)

if extracted_info == OWNER_INFO:
    print("SUCCESS: Ownership information verified.")
else:
    print("FAILURE: Ownership information does not match.")

# --------------------------------------------------
# 7. DISPLAY COMPARISON
# --------------------------------------------------

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.imshow(image_array)
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(watermarked_array)
plt.title("Copyright Watermarked Image")
plt.axis("off")

plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "copyright_comparison.png")
)
plt.show()

print("\nPractical 8 completed successfully!")
