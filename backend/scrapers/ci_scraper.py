from bs4 import BeautifulSoup as bs
import requests
from pdfquery import PDFQuery
import os

def open_pdf(pdf_path):
    pdf = PDFQuery(pdf_path)
    pdf.load()
    print(pdf.get_page(1))
    #text_elements = pdf.pq()
    #text = [t.text for t in text_elements]
    #print(text)

dir_path = os.path.dirname(os.path.realpath(__file__))
pdf_path = os.path.join(dir_path, 'pdfs', 'fall2024-ci.pdf')
open_pdf(pdf_path)