# import fitz  # PyMuPDF
# import pytesseract
# from pdf2image import convert_from_path
# from PIL import Image
# import os

# # 🔧 Set path if needed (Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# # ---------------- IMAGE OCR ----------------
# def ocr_image(image: Image.Image):
#     image = image.convert("L")  # grayscale
#     image = image.resize((image.width * 2, image.height * 2))

#     text = pytesseract.image_to_string(
#         image,
#         config="--oem 3 --psm 6"
#     )

#     return text.strip()


# # ---------------- DIGITAL PDF ----------------
# def extract_digital_text(pdf_path):
#     text = ""
#     doc = fitz.open(pdf_path)

#     for page in doc:
#         page_text = page.get_text()
#         if page_text:
#             text += page_text + "\n"

#     return text.strip()


# # ---------------- SCANNED PDF ----------------
# def extract_scanned_text(pdf_path):
#     text = ""

#     try:
#         pages = convert_from_path(pdf_path)

#         for page in pages:
#             text += ocr_image(page) + "\n"

#     except Exception as e:
#         print("⚠️ PDF2IMAGE failed:", e)

#     return text.strip()


# # ---------------- HYBRID PROCESSOR ----------------
# def extract_text(file_path):
#     ext = os.path.splitext(file_path)[1].lower()

#     # ---------------- IMAGE ----------------
#     if ext in [".png", ".jpg", ".jpeg"]:
#         print("📷 Processing image OCR...")
#         image = Image.open(file_path)
#         return ocr_image(image)

#     # ---------------- PDF ----------------
#     elif ext == ".pdf":
#         print("📄 Processing PDF...")

#         digital_text = ""
#         ocr_text = ""

#         # 🔹 Step 1: Try digital extraction
#         try:
#             digital_text = extract_digital_text(file_path)
#         except Exception as e:
#             print("⚠️ Digital extraction failed:", e)

#         # 🔹 Step 2: Decide if OCR needed
#         if len(digital_text.strip()) > 100:
#             print("✅ Digital PDF detected")

#             # 🔥 OPTIONAL: also OCR for missing parts
#             try:
#                 ocr_text = extract_scanned_text(file_path)
#             except:
#                 pass

#             # Combine both (helps in tables)
#             final_text = digital_text + "\n" + ocr_text

#         else:
#             print("🧾 Scanned PDF detected → using OCR")

#             final_text = extract_scanned_text(file_path)

#         return final_text.strip()

#     # ---------------- INVALID ----------------
#     else:
#         raise ValueError("Unsupported file type")


import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import os

# 🔧 Windows Tesseract path (change if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ---------------- TEXT CLEANER ----------------
def normalize_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.split())


# ---------------- OCR IMAGE ----------------
def ocr_image(image: Image.Image) -> str:
    image = image.convert("L")  # grayscale
    image = image.resize((image.width * 2, image.height * 2))

    text = pytesseract.image_to_string(
        image,
        config="--oem 3 --psm 6"
    )

    return normalize_text(text)


# ---------------- DIGITAL PAGE VALIDATION ----------------
def is_valid_digital(text: str) -> bool:
    if not text:
        return False

    words = text.split()
    if len(words) < 30:
        return False

    # check readable ratio
    alpha_ratio = sum(c.isalpha() for c in text) / max(len(text), 1)

    return alpha_ratio > 0.6


# ---------------- DIGITAL PDF EXTRACT ----------------
def extract_digital_text_page(page) -> str:
    try:
        return normalize_text(page.get_text())
    except:
        return ""


# ---------------- SCANNED PAGE OCR ----------------
def ocr_pdf_page(page) -> str:
    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return ocr_image(img)


# ---------------- HYBRID PDF PROCESSOR ----------------
def extract_pdf_hybrid(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)

    final_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Step 1: digital extraction
        digital_text = extract_digital_text_page(page)

        # Step 2: decide
        if is_valid_digital(digital_text):
            final_text.append(digital_text)
        else:
            try:
                ocr_text = ocr_pdf_page(page)
                final_text.append(ocr_text)
            except Exception as e:
                print(f"⚠️ OCR failed on page {page_num}: {e}")

    return normalize_text("\n".join(final_text))


# ---------------- IMAGE PROCESSOR ----------------
def extract_image_text(file_path: str) -> str:
    image = Image.open(file_path)
    return ocr_image(image)


# ---------------- MAIN ENTRY FUNCTION ----------------
def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()

    # ---------------- IMAGE ----------------
    if ext in [".png", ".jpg", ".jpeg"]:
        print("📷 Processing IMAGE OCR...")
        return extract_image_text(file_path)

    # ---------------- PDF ----------------
    elif ext == ".pdf":
        print("📄 Processing HYBRID PDF extraction...")
        return extract_pdf_hybrid(file_path)

    # ---------------- INVALID ----------------
    else:
        raise ValueError("Unsupported file type")