import os
import numpy as np
from PIL import Image
from scipy.fft import dct, idct

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

INPUT_PATH = "Practical_05_Robust_vs_Fragile_Watermarking/input/original.png"
OUTPUT_DIR = "Practical_05_Robust_vs_Fragile_Watermarking/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# LOAD IMAGE
# --------------------------------------------------

original = Image.open(INPUT_PATH).convert("L")
image = np.array(original, dtype=np.float64)

# Crop dimensions to multiples of 8 for block DCT
h, w = image.shape
h = (h // 8) * 8
w = (w // 8) * 8
image = image[:h, :w]

# --------------------------------------------------
# 1. ROBUST WATERMARKING USING DCT
# --------------------------------------------------

def embed_robust_watermark(image):
    result = image.copy()

    # A simple binary watermark pattern
    watermark = np.array([
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 0, 0],
        [0, 0, 1, 1]
    ])

    # Embed watermark bits in selected DCT coefficients
    strength = 20

    for i in range(4):
        for j in range(4):
            y = i * 8
            x = j * 8

            block = result[y:y+8, x:x+8]

            coeff = dct(dct(block, axis=0, norm="ortho"),
                        axis=1, norm="ortho")

            # Use a mid-frequency coefficient
            if watermark[i, j] == 1:
                coeff[3, 3] = abs(coeff[3, 3]) + strength
            else:
                coeff[3, 3] = -abs(coeff[3, 3]) - strength

            reconstructed = idct(
                idct(coeff, axis=1, norm="ortho"),
                axis=0, norm="ortho"
            )

            result[y:y+8, x:x+8] = reconstructed

    return np.clip(result, 0, 255).astype(np.uint8)


def extract_robust_watermark(image):
    watermark = np.zeros((4, 4), dtype=np.uint8)

    for i in range(4):
        for j in range(4):
            y = i * 8
            x = j * 8

            block = image[y:y+8, x:x+8].astype(np.float64)

            coeff = dct(dct(block, axis=0, norm="ortho"),
                        axis=1, norm="ortho")

            watermark[i, j] = 1 if coeff[3, 3] >= 0 else 0

    return watermark


# --------------------------------------------------
# 2. FRAGILE WATERMARKING USING LSB
# --------------------------------------------------

def embed_fragile_watermark(image):
    result = image.astype(np.uint8).copy()

    watermark = np.array([
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 0, 0],
        [0, 0, 1, 1]
    ])

    flat = result.flatten()

    for i, bit in enumerate(watermark.flatten()):
        flat[i] = (int(flat[i]) & 254) | int(bit)

    return flat.reshape(result.shape).astype(np.uint8)


def extract_fragile_watermark(image):
    flat = image.flatten()
    bits = flat[:16] & 1
    return bits.reshape(4, 4)


# --------------------------------------------------
# 3. IMAGE ATTACKS
# --------------------------------------------------

def add_noise(image):
    noise = np.random.normal(0, 15, image.shape)
    return np.clip(image.astype(float) + noise, 0, 255).astype(np.uint8)


def apply_jpeg_compression(image):
    temp_path = os.path.join(OUTPUT_DIR, "temp.jpg")
    Image.fromarray(image).save(temp_path, quality=40)
    compressed = np.array(Image.open(temp_path).convert("L"))
    os.remove(temp_path)
    return compressed


def apply_cropping(image):
    h, w = image.shape
    cropped = image[0:int(h * 0.9), 0:int(w * 0.9)]

    # Resize back to original dimensions for comparison
    return np.array(
        Image.fromarray(cropped).resize((w, h))
    )


# --------------------------------------------------
# 4. WATERMARK COMPARISON
# --------------------------------------------------

robust_image = embed_robust_watermark(image)
fragile_image = embed_fragile_watermark(image)

Image.fromarray(robust_image).save(
    f"{OUTPUT_DIR}/robust_watermarked.png"
)

Image.fromarray(fragile_image).save(
    f"{OUTPUT_DIR}/fragile_watermarked.png"
)

# Original watermark patterns
original_robust_mark = extract_robust_watermark(robust_image)
original_fragile_mark = extract_fragile_watermark(fragile_image)

attacks = {
    "Noise": add_noise,
    "JPEG Compression": apply_jpeg_compression,
    "Cropping": apply_cropping
}

print("\nWATERMARK ATTACK COMPARISON")
print("=" * 60)

for attack_name, attack_function in attacks.items():

    attacked_robust = attack_function(robust_image)
    attacked_fragile = attack_function(fragile_image)

    extracted_robust = extract_robust_watermark(attacked_robust)
    extracted_fragile = extract_fragile_watermark(attacked_fragile)

    robust_accuracy = np.mean(
        extracted_robust == original_robust_mark
    ) * 100

    fragile_accuracy = np.mean(
        extracted_fragile == original_fragile_mark
    ) * 100

    print(f"\nAttack: {attack_name}")
    print(f"Robust watermark accuracy: {robust_accuracy:.2f}%")
    print(f"Fragile watermark accuracy: {fragile_accuracy:.2f}%")

    Image.fromarray(attacked_robust).save(
        f"{OUTPUT_DIR}/robust_{attack_name.lower().replace(' ', '_')}.png"
    )

    Image.fromarray(attacked_fragile).save(
        f"{OUTPUT_DIR}/fragile_{attack_name.lower().replace(' ', '_')}.png"
    )

print("\nPractical 5 completed!")
