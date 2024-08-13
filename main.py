import os
from PIL import Image
import pytesseract

# Path to the directory containing image files
directory_path = r'E:\Project\images'

# Supported image file extensions
image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

# Function to extract and process text from an image file
def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra spaces
        text = ' '.join(text.split())
        
        return text
    except Exception as e:
        print(f"Could not process {image_path}: {e}")
        return None

# Iterate over all files in the directory
for filename in os.listdir(directory_path):
    if filename.lower().endswith(image_extensions):
        file_path = os.path.join(directory_path, filename)
        print(f"Processing file: {file_path}")
        extracted_text = extract_text_from_image(file_path)
        if extracted_text:
            print(f"Extracted text from {filename}:\n{extracted_text}\n")
