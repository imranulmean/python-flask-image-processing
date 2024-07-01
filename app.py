from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
from PIL import Image
import io
import math

# app instance
app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'  # Define the folder where uploaded files are stored
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

def compress_img(image_data, new_size_ratio=0.9, quality=15, width=None, height=None, to_jpg=True):

    img = Image.open(io.BytesIO(image_data))
    # Convert RGBA image to RGB
    if img.mode == 'RGBA':
        img = img.convert('RGB')    
    print("[*] Image shape:", img.size)
    image_size = len(image_data)
    print("[*] Size before compression:", get_size_format(image_size))
    if new_size_ratio < 1.0:
        img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)))
        print("[+] New Image shape:", img.size)
    elif width and height:
        img = img.resize((width, height))
        print("[+] New Image shape:", img.size)
    new_image_data = io.BytesIO()
    if to_jpg:
        img.save(new_image_data, format='JPEG', quality=quality, optimize=True)
    else:
        img.save(new_image_data, format=img.format, quality=quality, optimize=True)
    print("[+] Image compressed.")
    new_image_size = new_image_data.tell()
    print("[+] Size after compression:", get_size_format(new_image_size))
    saving_diff = image_size - new_image_size
    print(f"[+] Image size change: {saving_diff/image_size*100:.2f}% of the original image size.")
    return new_image_data.getvalue()

# /api/home
# @app.route("/api/home", methods=['GET'])
# def return_home():
#     return jsonify({
#         'message': "Like this video if this helped!",
#         'people': ['Jack', 'Harry', 'Arpan']
#     })

@app.route("/api/ping",methods=["GET"])
def test():
    a="pong"
    return jsonify(a)

# @app.route('/api/upload', methods=['POST'])
# def upload():       
#        if 'photo' not in request.files:
#         return {'error': 'No file part'}, 400

#        file = request.files['photo']
#        print(file.filename) 
#        if file.filename == '':
#         return {'error': 'No selected file'}, 400

#        file.save('uploads/' + file.filename)
#        return jsonify({
#            "msg":"File Uploaded Succecfully",
#            "fileName": file.filename

#        })

# Image not Saved in folder but in Buffer

@app.route('/api/upload', methods=['POST'])
def upload():
    if 'photo' not in request.files:
        return {'error': 'No file part'}, 400

    file = request.files['photo']

    if file.filename == '':
        return {'error': 'No selected file'}, 400

    # Read the image file into memory
    image_data = file.read()

    # Compress the image in memory
    compressed_image_data = compress_img(image_data)
    return send_file(io.BytesIO(compressed_image_data), mimetype='image/jpeg', as_attachment=True, download_name='compressed_image.jpg')

# Route to serve download files
@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/image_to_pdf', methods=['POST'])
def image_to_pdf():
    if 'images' not in request.files:
        return 'No files part', 400

    images = request.files.getlist('images')
    if len(images) == 0:
        return 'No files selected', 400

    pages = int(request.form.get('pages', 1))

    # Open images and create a list of Image objects
    img_list = [Image.open(img).convert('RGB') for img in images]

    # Calculate the number of images per page
    imgs_per_page = math.ceil(len(img_list) / pages)

    pdf_pages = []
    for i in range(pages):
        # Get the images for the current page
        page_images = img_list[i*imgs_per_page:(i+1)*imgs_per_page]
        
        if not page_images:
            break

        # Calculate the max width and total height for the current page
        widths, heights = zip(*(img.size for img in page_images))
        max_width = max(widths)
        total_height = sum(heights)

        # Create a new blank image with the calculated dimensions
        pdf_page = Image.new('RGB', (max_width, total_height))

        # Paste all images into the blank image
        y_offset = 0
        for img in page_images:
            pdf_page.paste(img, (0, y_offset))
            y_offset += img.size[1]

        pdf_pages.append(pdf_page)

    # Create a BytesIO object to hold the PDF data
    pdf_bytes = io.BytesIO()
    pdf_pages[0].save(pdf_bytes, format='PDF', save_all=True, append_images=pdf_pages[1:])
    pdf_bytes.seek(0)

    # Send the PDF back to the client
    return send_file(pdf_bytes, mimetype='application/pdf', as_attachment=True, download_name='output.pdf')

if __name__ == "__main__":
    app.run(debug=True, port=8080)