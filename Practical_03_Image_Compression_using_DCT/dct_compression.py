
from PIL import Image
import numpy as np
from scipy.fft import dct, idct

# ==========================================
# STEP 1: LOAD ORIGINAL IMAGE
# ==========================================

image_path = "Practical_03_Image_Compression_using_DCT/input/original.png"

image = Image.open(image_path).convert("L")
image_array = np.array(image)

print("Original image dimensions:", image_array.shape)


# ==========================================
# STEP 2: CROP IMAGE TO MULTIPLES OF 8
# ==========================================

height, width = image_array.shape

new_height = (height // 8) * 8
new_width = (width // 8) * 8

image_array = image_array[:new_height, :new_width]

print("Cropped image dimensions:", image_array.shape)


# ==========================================
# STEP 3: CREATE EMPTY RECONSTRUCTED IMAGE
# ==========================================

reconstructed_image = np.zeros(
    (new_height, new_width),
    dtype=float
)


# ==========================================
# STEP 4: PROCESS EACH 8x8 BLOCK
# ==========================================

for y in range(0, new_height, 8):

    for x in range(0, new_width, 8):

        # Extract 8x8 block
        block = image_array[y:y+8, x:x+8].astype(float)

        # Apply 2D DCT
        dct_block = dct(
            dct(block, axis=0, norm='ortho'),
            axis=1,
            norm='ortho'
        )

        # ==================================
        # STEP 5: REMOVE HIGH FREQUENCIES
        # ==================================

        compressed_dct = dct_block.copy()

        # Retain only top-left 4x4 coefficients
        compressed_dct[4:, :] = 0
        compressed_dct[:, 4:] = 0

        # ==================================
        # STEP 6: APPLY INVERSE DCT
        # ==================================

        reconstructed_block = idct(
            idct(compressed_dct, axis=1, norm='ortho'),
            axis=0,
            norm='ortho'
        )

        # Place reconstructed block in output image
        reconstructed_image[y:y+8, x:x+8] = reconstructed_block


# ==========================================
# STEP 7: CONVERT PIXEL VALUES TO UINT8
# ==========================================

reconstructed_image = np.clip(
    np.round(reconstructed_image),
    0,
    255
).astype(np.uint8)


# ==========================================
# STEP 8: SAVE RECONSTRUCTED IMAGE
# ==========================================

output_path = "Practical_03_Image_Compression_using_DCT/output/reconstructed.png"

output_image = Image.fromarray(reconstructed_image)
output_image.save(output_path)

print("\nDCT compression process completed!")
print("Reconstructed image saved successfully.")


# ==========================================
# STEP 9: CALCULATE IMAGE QUALITY
# ==========================================

original = image_array.astype(float)
reconstructed = reconstructed_image.astype(float)

# Mean Squared Error
mse = np.mean((original - reconstructed) ** 2)

# Peak Signal-to-Noise Ratio
if mse == 0:
    psnr = float("inf")
else:
    psnr = 10 * np.log10((255 ** 2) / mse)

print("\nImage Quality Results:")
print("MSE:", round(mse, 2))
print("PSNR:", round(psnr, 2), "dB")

print("\nOriginal image size:", image_array.shape)
print("Reconstructed image size:", reconstructed_image.shape)


# ==========================================
# STEP 10: DISPLAY BOTH IMAGES
# ==========================================

Image.fromarray(image_array).show()
output_image.show()
