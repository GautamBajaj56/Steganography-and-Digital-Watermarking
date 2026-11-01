
from PIL import Image, ImageDraw, ImageFont

# Step 1: Load the original image
image = Image.open("./input/original.png").convert("RGB")

# Step 2: Create a drawing object
draw = ImageDraw.Draw(image)

# Step 3: Define watermark text
watermark_text = "NSUT | Digital Watermarking"

# Step 4: Load font
font = ImageFont.truetype("./fonts/Arial.ttf", 35)

# Step 5: Calculate text position
width, height = image.size
text_width = draw.textbbox((0, 0), watermark_text, font=font)[2]
text_height = draw.textbbox((0, 0), watermark_text, font=font)[3]

x = width - text_width - 30
y = height - text_height - 30

# Step 6: Draw watermark on image
draw.text((x, y), watermark_text, fill="white", font=font)

# Step 7: Save watermarked image
image.save("./output/visible_watermarked.png")

print("Visible watermark embedded successfully!")
