import cv2
import numpy as np

class ImageExtractor:
    @staticmethod
    def extract_images(images):
        extracted_images = []
        for image in images:
            image_np = np.array(image)
            gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                roi = image_np[y:y+h, x:x+w]
                extracted_images.append(roi)
        return extracted_images
