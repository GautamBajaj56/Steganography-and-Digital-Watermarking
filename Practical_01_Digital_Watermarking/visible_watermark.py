
from PIL import Image, ImageDraw, ImageFont

# --------------------------------
# PART 1: VISIBLE WATERMARK EMBEDDING
# --------------------------------

# Step 1: Load the original image
image_path = "Practical_01_Digital_Watermarking/input/original.png"
image = Image.open(image_path).convert("RGB")

# Step 2: Define watermark text
watermark_text = "NSUT | Digital Watermarking"

# Step 3: Load font
font = ImageFont.truetype(
    "/System/Library/Fonts/Supplemental/Arial.ttf", 35
)

# Step 4: Calculate watermark position
draw = ImageDraw.Draw(image)
width, height = image.size

bbox = draw.textbbox((0, 0), watermark_text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

x = width - text_width - 30
y = height - text_height - 30

# Step 5: Embed watermark
draw.text(
    (x, y),
    watermark_text,
    fill="white",
    font=font
)

# Step 6: Save watermarked image
output_path = "Practical_01_Digital_Watermarking/output/visible_watermarked.png"
image.save(output_path)

print("Visible watermark embedded successfully!")

# --------------------------------
# PART 2: WATERMARK RETRIEVAL
# --------------------------------

# Step 7: Open the watermarked image
watermarked_image = Image.open(output_path)

# Step 8: Display the watermarked image
watermarked_image.show()

print("Watermarked image opened successfully.")
print("Watermark text:", watermark_text)
