from core.extractors.pdf import PDFExtractor
from core.extractors.text import TextExtractor

EXTRACTORS = [
    PDFExtractor(),
    TextExtractor(),
]

def extract_text(file):
    for ex in EXTRACTORS:
        if ex.supports(file.name):
            return ex.extract(file)
    return ""
