
from PIL import Image, ImageDraw, ImageFont

# Load original image
image = Image.open(
    "Practical_01_Digital_Watermarking/input/original.png"
).convert("RGBA")

# Create a transparent layer
watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))

# Create drawing object
draw = ImageDraw.Draw(watermark_layer)

# Define watermark
watermark_text = "NSUT | Digital Watermarking"

# Load font
font = ImageFont.truetype(
    "/System/Library/Fonts/Supplemental/Arial.ttf", 35
)

# Calculate position
width, height = image.size
bbox = draw.textbbox((0, 0), watermark_text, font=font)

text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]

x = width - text_width - 30
y = height - text_height - 30

# Draw semi-transparent watermark
draw.text(
    (x, y),
    watermark_text,
    fill=(255, 255, 255, 128),
    font=font
)

# Blend watermark layer with original image
watermarked_image = Image.alpha_composite(image, watermark_layer)

# Save output
watermarked_image.convert("RGB").save(
    "Practical_01_Digital_Watermarking/output/transparent_watermarked.png"
)

print("Semi-transparent watermark embedded successfully!")
