import pytesseract
from PIL import Image
import fitz
import cv2
import numpy as np
from pdf2image import convert_from_path


def detect_images_in_pdf(pdf_file):
    # Konwertowanie PDF do obrazów
    pages = convert_from_path(pdf_file, dpi=300)

    for page_num, page in enumerate(pages):
        # Konwertuj stronę na tablicę NumPy dla OpenCV
        page_np = np.array(page)

        # Przekształć obraz na skalę szarości
        gray = cv2.cvtColor(page_np, cv2.COLOR_RGB2GRAY)

        # Zbinaryzuj obraz (próg)
        _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

        # Znajdź kontury, które mogą być obrazami
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Wycinanie obrazów
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            roi = page_np[y:y + h, x:x + w]

            # Zapisz wykryty obraz
            cv2.imwrite(f'image_{page_num}_{x}_{y}.png', roi)

def pdf_to_hocr(pdf_file):
    # Otwórz plik PDF
    doc = fitz.open(pdf_file)

    hocr_data = ""

    # Iteruj przez każdą stronę i konwertuj na obraz
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Przetwórz obraz do HOCR
        hocr_data += pytesseract.image_to_pdf_or_hocr(img, extension='hocr').decode('utf-8')

    # Zapisz wynikowy plik HOCR
    with open('output.hocr', 'w', encoding='utf-8') as f:
        f.write(hocr_data)


def image_to_hocr(image):
    # Przetwórz obraz do formatu HOCR
    hocr_data = pytesseract.image_to_pdf_or_hocr(image, extension='hocr')
    # Zapisz wynik do pliku .hocr
    with open('output.hocr', 'wb') as f:
        f.write(hocr_data)

# Przetwarzanie zeskanowanego PDF
pdf_to_hocr('scanned_document.pdf')