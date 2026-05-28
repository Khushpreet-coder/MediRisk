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

# import re

# def clean_text(text: str) -> str:
#     if not text:
#         return ""

#     # remove weird OCR artifacts
#     text = text.replace("\n", " ")
#     text = re.sub(r"\s+", " ", text)

#     # fix broken spacing in numbers (e.g., "14 . 5" → "14.5")
#     text = re.sub(r"(\d)\s*\.\s*(\d)", r"\1.\2", text)

#     # remove non-printable chars
#     text = re.sub(r"[^\x20-\x7E]+", " ", text)

#     return text.strip()


import re


OCR_NOISE = [
    "Photometry",
    "Calculated",
    "Electrical Impedence",
    "Flow Cytometry",
    "FCM/",
    "Microscopy"
]


# =====================================
# MEDICAL TEXT CLEANING FUNCTIONS
# =====================================

def fix_common_ocr_misreadings(text: str) -> str:
    """
    Fix common OCR errors specific to medical reports.
    Context-aware replacements to avoid breaking actual words.
    """
    
    # Fix common character confusions in medical context
    replacements = [
        # Only replace single 'l' or 'O' in numeric contexts
        (r'(?<![a-z])l(?=\d)', '1'),  # 'l' → '1' before numbers
        (r'(?<!\d)O(?=\d)', '0'),     # 'O' → '0' when followed by numbers
        (r'(?<=[0-9])([l])(?=[0-9])', '1'),  # 'l' between numbers → '1'
    ]
    
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text)
    
    return text


def normalize_medical_numbers(text: str) -> str:
    """
    Smarter normalization for medical numeric values.
    """

    # ---------------------------------
    # CASE 1:
    # Decimal commas → decimal points
    # Example: 13,5 -> 13.5
    # Only when 1-2 digits after comma
    # ---------------------------------
    text = re.sub(
        r'(?<=\d),(?=\d{1,2}\b)',
        '.',
        text
    )

    # ---------------------------------
    # CASE 2:
    # Thousand separators
    # Example: 5.100 -> 5100
    # Example: 10.800 -> 10800
    # ONLY for large medical counts
    # ---------------------------------
    text = re.sub(
        r'\b(\d{1,2})\.(\d{3})\b',
        r'\1\2',
        text
    )

    # ---------------------------------
    # Fix broken decimals
    # ---------------------------------
    text = re.sub(
        r'(\d)\s*\.\s*(\d)',
        r'\1.\2',
        text
    )

    # ---------------------------------
    # Normalize ranges
    # ---------------------------------
    text = re.sub(
        r'(\d+\.?\d*)\s*[=~:]\s*(\d+\.?\d*)',
        r'\1 - \2',
        text
    )

    text = re.sub(
        r'(\d+\.?\d*)\s*[-–—~]\s*(\d+\.?\d*)',
        r'\1 - \2',
        text
    )

    # ---------------------------------
    # Remove duplicate dots
    # ---------------------------------
    text = re.sub(r'\.{2,}', '.', text)

    return text


def normalize_whitespace(text: str) -> str:
    """
    Clean up whitespace while preserving structure.
    Removes excessive spaces but keeps line breaks for table structure.
    """
    
    if not text:
        return ""
    
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Remove excessive spaces within line
        line = re.sub(r'\s+', ' ', line).strip()
        
        # Skip empty lines
        if line:
            cleaned_lines.append(line)
    
    # Join back with preserved line structure
    return '\n'.join(cleaned_lines)


# =====================================
# MAIN CLEANING FUNCTION
# =====================================

def clean_text(text: str) -> str:
    """
    Main cleaning pipeline for OCR output.
    Preserves medical data integrity while fixing OCR artifacts.
    """
    
    if not text:
        return ""
    
    # Step 1: Fix common OCR character confusion
    text = fix_common_ocr_misreadings(text)
    
    # Step 2: Normalize numeric values and ranges
    text = normalize_medical_numbers(text)
    
    # Step 3: Clean up whitespace and structure
    text = normalize_whitespace(text)
    
    # Step 4: Remove obvious noise artifacts
    for noise in OCR_NOISE:
        text = re.sub(rf'\b{re.escape(noise)}\b', '', text, flags=re.IGNORECASE)
    
    # Step 5: Final whitespace cleanup
    text = normalize_whitespace(text)
    
    return text


