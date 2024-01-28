import cv2
from pyzbar.pyzbar import decode

# Function to decode QR code from an image file
def decode_qr_code(image_path):
    image = cv2.imread(image_path)
    qr_codes = decode(image)
    
    decoded_data = []
    for qr_code in qr_codes:
        data = qr_code.data.decode('utf-8')
        decoded_data.append(data)
    
    return decoded_data

# Iterate over your QR code images and decode them
for i in range(1000):  # Adjust the range based on your file names
    image_path = f'path/to/your/folder/frame_{i:03d}.png'  # Adjust the path and file format
    try:
        decoded_data = decode_qr_code(image_path)
        print(f"Decoded data from {image_path}: {decoded_data}")
    except Exception as e:
        print(f"Error decoding {image_path}: {e}")

