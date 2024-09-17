import os
from pdf2image import convert_from_path
from PIL import Image


class FileProcessor:
    def __init__(self):
        self.images = []

    def load_files(self, file_paths):
        """Załaduj obrazy lub konwertuj PDF na obrazy"""
        for file in file_paths:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff')):
                self.images.append(Image.open(file))
            elif file.lower().endswith('.pdf'):
                self.images.extend(convert_from_path(file, dpi=300))

    def get_images(self):
        """Zwraca listę obrazów do dalszego przetwarzania"""
        return self.images
