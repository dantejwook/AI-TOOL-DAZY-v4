import pdfplumber
from core.extractors.base import BaseExtractor

class PDFExtractor(BaseExtractor):
    def supports(self, filename):
        return filename.lower().endswith(".pdf")

    def extract(self, file):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages[:5]:
                text += page.extract_text() or ""
        return text
