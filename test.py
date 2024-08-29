"""Testing OCR tools to extract text from PDFs"""
import os

#Libs to extract text from files
import PyPDF2
from pdf2image import convert_from_path

#Lib for OCR
import pytesseract

# pylint: disable=C0116
# pylint: disable=C0200

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        if reader.is_encrypted:
            reader.decrypt('')
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = page.extract_text()
            if page_text:
                text += page_text
            else:
                # If no text is found, use OCR on that specific page
                images = convert_from_path(
                    pdf_path=pdf_path,
                    first_page=page_num + 1,
                    last_page=page_num + 1)

                #@TODO IF OS is MacOS - Use script to send it over to Native OCR instead of using pytesseract
                text += pytesseract.image_to_string(images[0])
    return text

def process_pdfs(input_folder: str, output_folder: str) -> None:
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            print(f"Processing {filename}...")

            # Extract text using a combination of PyPDF2 and OCR
            text = extract_text_from_pdf(pdf_path)

            # Save the output text to a file
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.txt")
            with open(output_path, 'w', encoding='utf-8') as text_file:
                text_file.write(text)

            print(f"Text extracted to {output_path}")

# Set the input and output directories
PDF_FOLDER = './myPdfs'
TXT_FOLDER = './myTxts'

process_pdfs(PDF_FOLDER, TXT_FOLDER)
