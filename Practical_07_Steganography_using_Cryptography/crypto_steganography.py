
import os
import numpy as np
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

INPUT_PATH = "Practical_07_Steganography_using_Cryptography/input/original.png"
OUTPUT_DIR = "Practical_07_Steganography_using_Cryptography/output"

OUTPUT_PATH = os.path.join(OUTPUT_DIR, "stego_image.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# 1. AES ENCRYPTION
# --------------------------------------------------

def encrypt_message(message, key):

    cipher = AES.new(key, AES.MODE_GCM)

    ciphertext, tag = cipher.encrypt_and_digest(
        message.encode("utf-8")
    )

    # Store nonce + authentication tag + ciphertext
    encrypted_data = cipher.nonce + tag + ciphertext

    return encrypted_data


# --------------------------------------------------
# 2. AES DECRYPTION
# --------------------------------------------------

def decrypt_message(encrypted_data, key):

    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

    return decrypted_data.decode("utf-8")


# --------------------------------------------------
# 3. HIDE ENCRYPTED DATA USING LSB
# --------------------------------------------------

def hide_data(image_array, data):

    binary_data = ''.join(
        format(byte, '08b') for byte in data
    )

    # 32-bit header stores the payload length in bytes
    length_header = format(len(data), '032b')

    binary_data = length_header + binary_data

    flat_image = image_array.reshape(-1).copy()

    if len(binary_data) > len(flat_image):
        raise ValueError(
            "Image capacity is insufficient for this message."
        )

    for i, bit in enumerate(binary_data):
        flat_image[i] = (
            (int(flat_image[i]) & 254) | int(bit)
        )

    return flat_image.reshape(image_array.shape).astype(np.uint8)


# --------------------------------------------------
# 4. EXTRACT ENCRYPTED DATA USING LSB
# --------------------------------------------------

def extract_data(image_array):

    flat_image = image_array.reshape(-1)

    # Extract 32-bit payload length
    length_bits = ''.join(
        str(int(value) & 1)
        for value in flat_image[:32]
    )

    payload_length = int(length_bits, 2)

    required_bits = 32 + payload_length * 8

    if required_bits > len(flat_image):
        raise ValueError("Invalid or incomplete hidden payload.")

    # Extract encrypted payload
    payload_bits = ''.join(
        str(int(value) & 1)
        for value in flat_image[32:required_bits]
    )

    encrypted_data = bytes(
        int(payload_bits[i:i+8], 2)
        for i in range(0, len(payload_bits), 8)
    )

    return encrypted_data


# --------------------------------------------------
# 5. MAIN PROGRAM
# --------------------------------------------------

# Load original image
original_image = Image.open(INPUT_PATH).convert("RGB")
image_array = np.array(original_image, dtype=np.uint8)

# Generate a 256-bit AES key
key = get_random_bytes(32)

# Original secret message
secret_message = "NSUT SECRET MESSAGE - STEGANOGRAPHY PRACTICAL 7"

print("\nORIGINAL MESSAGE:")
print(secret_message)

# Encrypt message
encrypted_data = encrypt_message(secret_message, key)

print("\nAES ENCRYPTION")
print("Encrypted payload size:", len(encrypted_data), "bytes")

# Hide encrypted data inside image
stego_array = hide_data(image_array, encrypted_data)

Image.fromarray(stego_array).save(OUTPUT_PATH)

print("\nSTEGANOGRAPHY")
print("Encrypted message successfully hidden inside image.")
print("Stego image saved at:", OUTPUT_PATH)

# --------------------------------------------------
# 6. EXTRACT AND DECRYPT
# --------------------------------------------------

stego_image = Image.open(OUTPUT_PATH).convert("RGB")
stego_array = np.array(stego_image, dtype=np.uint8)

extracted_data = extract_data(stego_array)

print("\nEXTRACTION")
print("Encrypted data extracted successfully.")

# Decrypt extracted data
recovered_message = decrypt_message(extracted_data, key)

print("\nAES DECRYPTION")
print("Recovered message:", recovered_message)

# Verify correctness
print("\nVERIFICATION")

if recovered_message == secret_message:
    print("SUCCESS: Original message recovered correctly!")
else:
    print("FAILURE: Message recovery unsuccessful.")

print("\nPractical 7 completed successfully!")
