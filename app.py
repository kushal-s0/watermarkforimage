from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

# Set a directory for uploaded images (temporary storage)
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the uploaded file and watermark text
    if 'image' not in request.files or 'watermark_text' not in request.form:
        return "No image or watermark text provided", 400

    file = request.files['image']
    watermark_text = request.form['watermark_text']

    # Open the uploaded image
    image = Image.open(file.stream)

    # Add watermark
    watermarked_image = add_watermark(image, watermark_text)

    # Save the watermarked image to a BytesIO object
    img_io = io.BytesIO()
    watermarked_image.save(img_io, 'PNG')
    img_io.seek(0)

    # Return the watermarked image
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="watermarked_image.png")

def add_watermark(image, text):
    # Make a copy of the original image to modify
    watermark_image = image.copy()
    draw = ImageDraw.Draw(watermark_image)

    # Load font, with a fallback in case 'arial.ttf' is unavailable
    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except IOError:
        font = ImageFont.load_default()

    # Calculate position for the watermark at the bottom right
    width, height = watermark_image.size
    # Use textbbox to get the bounding box of the text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x, y = width - text_width - 10, height - text_height - 10

    # Add the watermark text with transparency
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))
    return watermark_image

if __name__ == '__main__':
    app.run(debug=True)
