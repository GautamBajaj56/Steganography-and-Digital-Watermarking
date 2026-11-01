
from PIL import Image

# Step 1: Load the original image
image = Image.open(
    "Practical_01_Digital_Watermarking/input/original.png"
).convert("RGB")

# Step 2: Define the secret message
message = "NSUT DIGITAL WATERMARKING"

# Step 3: Convert message into binary
message_bytes = message.encode("utf-8")
binary_message = ''.join(
    format(byte, '08b') for byte in message_bytes
)

# Step 4: Add an end marker
binary_message += "11111111"

# Step 5: Check image capacity
width, height = image.size
total_capacity = width * height * 3

if len(binary_message) > total_capacity:
    raise ValueError("Image does not have enough capacity!")

# Step 6: Embed message into image pixels
data_index = 0

for y in range(height):
    for x in range(width):

        if data_index >= len(binary_message):
            break

        pixel = list(image.getpixel((x, y)))

        for channel in range(3):

            if data_index >= len(binary_message):
                break

            secret_bit = int(binary_message[data_index])

            pixel[channel] = (pixel[channel] & 254) | secret_bit

            data_index += 1

        image.putpixel((x, y), tuple(pixel))

    if data_index >= len(binary_message):
        break

# Step 7: Save the watermarked image
image.save(
    "Practical_01_Digital_Watermarking/output/invisible_watermarked.png",
    format="PNG"
)

print("Secret message embedded successfully!")
print("Message:", message)
print("Total bits embedded:", data_index)
