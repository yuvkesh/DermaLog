import cv2

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    resized = cv2.resize(image, (800, 600))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray)
    return denoised
