import pytesseract
from PIL import Image

def solve_captcha(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, config='--psm 8').strip()
        return ''.join(filter(str.isalnum, text))  # clean up non-alphanumerics
    except Exception as e:
        print(f"❌ OCR Error: {e}")
        return ""
