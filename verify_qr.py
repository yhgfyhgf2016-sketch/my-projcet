from PIL import Image
from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
import os

def verify_qr_code(pdf_path):
    try:
        images = convert_from_path(pdf_path)
        for i, image in enumerate(images):
            # Save the image temporarily to process it
            image_path = f"temp_page_{i}.png"
            image.save(image_path)
            
            decoded_objects = decode(Image.open(image_path))
            if decoded_objects:
                for obj in decoded_objects:
                    print("QR Code Data:", obj.data.decode("utf-8"))
                    os.remove(image_path)
                    return obj.data.decode("utf-8") # Return the first QR code found
            os.remove(image_path)
        return None # No QR code found in any page
    except Exception as e:
        print(f"Error verifying QR code: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    pdf_file = 'sample_certificate.pdf'
    qr_data = verify_qr_code(pdf_file)
    if qr_data:
        print(f"QR Code data from PDF: {qr_data}")
    else:
        print("No QR code found in the PDF or an error occurred.")


