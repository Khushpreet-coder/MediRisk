# import re

# def clean_text(text: str) -> str:
#     """
#     Cleans OCR noise WITHOUT destroying medical meaning
#     """

#     # Fix broken spacing
#     text = re.sub(r'\s+', ' ', text)

#     # Fix weird OCR symbols but KEEP numbers/units
#     text = re.sub(r'[^\x00-\x7F]+', ' ', text)

#     # Fix broken hyphen spacing
#     text = text.replace(" - ", "-")

#     # Remove repeated dots
#     text = re.sub(r'\.{2,}', '.', text)

#     return text.strip()

import re

def clean_text(text: str) -> str:
    if not text:
        return ""

    # remove weird OCR artifacts
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    # fix broken spacing in numbers (e.g., "14 . 5" → "14.5")
    text = re.sub(r"(\d)\s*\.\s*(\d)", r"\1.\2", text)

    # remove non-printable chars
    text = re.sub(r"[^\x20-\x7E]+", " ", text)

    return text.strip()