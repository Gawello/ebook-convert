import pytesseract

class TextExtractor:
    @staticmethod
    def extract_text(images):
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        return text
