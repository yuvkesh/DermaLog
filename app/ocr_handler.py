import pytesseract

def perform_ocr(image):
    text = pytesseract.image_to_string(image)
    return text
