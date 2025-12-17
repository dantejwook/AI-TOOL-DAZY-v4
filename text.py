from core.extractors.base import BaseExtractor

class TextExtractor(BaseExtractor):
    def supports(self, filename):
        return filename.lower().endswith((".txt", ".md"))

    def extract(self, file):
        return file.getvalue().decode("utf-8", errors="ignore")[:3000]
