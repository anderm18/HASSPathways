from bs4 import BeautifulSoup as bs
import requests
from pypdf import PdfReader
import os

def is_number(s: str) -> bool:
    try:
        num = int(s)
        return True 
    except:
        return False

def parse_page(page_text: str) -> list[str]:
    lines = page_text.split("\n")
    result = []
    for line in lines:
        words = line.split(" ")
        if len(words[0]) == 5 and is_number(words[0]):
            result.append(words[1].rsplit("-", 1)[0])
    return result

def parse_pdf(pdf_path: str) -> set[str]:
    pdf = PdfReader(pdf_path)
    cis = set()
    num_pages = len(pdf.pages)
    for i in range(num_pages):
        page = pdf.pages[i]
        text = page.extract_text()
        parsed = parse_page(text)
        [cis.add(i) for i in parsed]
    return cis

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pdf_path = os.path.join(dir_path, 'pdfs', 'fall2024-ci.pdf')
    parse_pdf(pdf_path)