"""
Init config for your project
Use pip install .
"""
from setuptools import setup, find_packages

setup(
    name='Triagem3-Python',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PyPDF2',
        'pdf2image',
        'pytesseract'
    ],
    author='Sumi',
    description='Learning project for OCR Tools',
    url='https://github.com/sumi-satsuo/OCR_Extraction_Tool',
)
