"""Testing OCR tools to extract text from PDFs"""
import os

#Libs to extract text from files
import PyPDF2
from pdf2image import convert_from_path

#Lib for OCR
import pytesseract

# pylint: disable=C0116

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        if reader.is_encrypted:
            reader.decrypt('')
        for page_num in enumerate(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def extract_text_from_scanned_pdf(pdf_path: str) -> str:
    images = convert_from_path(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def process_pdfs(input_folder: str, output_folder: str) -> None:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            print(f"Processing {filename}...")
            text = extract_text_from_pdf(pdf_path)

            if not text.strip():  # If text is empty, it might be a scanned PDF
                text = extract_text_from_scanned_pdf(pdf_path)

            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            print(f"Text extracted to {output_path}")

# Set the input and output directories
PDF_FOLDER = './myPdfs'
TXT_FOLDER = './myTxts'

process_pdfs(PDF_FOLDER, TXT_FOLDER)
