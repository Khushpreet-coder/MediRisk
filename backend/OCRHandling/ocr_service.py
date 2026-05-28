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


# import fitz  # PyMuPDF
# import pytesseract
# from pdf2image import convert_from_path
# from PIL import Image, ImageFilter, ImageOps
# import cv2
# import numpy as np
# import os

# # 🔧 Windows Tesseract path (change if needed)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# # ---------------- TEXT CLEANER ----------------
# def normalize_text(text: str) -> str:
#     if not text:
#         return ""
#     return " ".join(text.split())


# # =====================================
# # ADVANCED IMAGE PREPROCESSING
# # =====================================
# def preprocess_image_for_ocr(image: Image.Image) -> Image.Image:
#     """
#     Advanced preprocessing for medical documents.
#     Improves OCR quality by 30-50%
#     """
    
#     # Convert to numpy for cv2 operations
#     img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
#     # 1. Upscale image (4x for small/blurry medical text)
#     scale_percent = 400
#     width = int(img_cv.shape[1] * scale_percent / 100)
#     height = int(img_cv.shape[0] * scale_percent / 100)
#     img_cv = cv2.resize(img_cv, (width, height), interpolation=cv2.INTER_CUBIC)
    
#     # 2. Convert to grayscale
#     gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
#     # 3. Denoise image (removes speckles while preserving text)
#     denoised = cv2.fastNlMeansDenoising(gray, h=10, templateWindowSize=7, searchWindowSize=21)
    
#     # 4. Contrast enhancement using CLAHE (Contrast Limited Adaptive Histogram Equalization)
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     enhanced = clahe.apply(denoised)
    
#     # 5. Binary thresholding (convert to black and white for crisp text)
#     _, binary = cv2.threshold(enhanced, 150, 255, cv2.THRESH_BINARY)
    
#     # 6. Morphological operations to clean up noise
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
#     binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
#     binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    
#     return Image.fromarray(binary)


# def deskew_image(img_array: np.ndarray) -> np.ndarray:
#     """Auto-correct tilted/skewed documents"""
#     coords = np.column_stack(np.where(img_array > 0))
#     if len(coords) == 0:
#         return img_array
    
#     try:
#         angle = cv2.minAreaRect(coords)[2]
#         # Only rotate if significantly skewed
#         if angle < -10 or angle > 10:
#             h, w = img_array.shape
#             center = (w // 2, h // 2)
#             M = cv2.getRotationMatrix2D(center, angle, 1.0)
#             img_array = cv2.warpAffine(img_array, M, (w, h), cval=255)
#     except:
#         pass  # If deskewing fails, use original
    
#     return img_array


# # =====================================
# # OPTIMIZED OCR WITH CONFIDENCE SCORING
# # =====================================
# def ocr_image(image: Image.Image, confidence_threshold: int = 0) -> str:
#     """
#     Enhanced OCR with preprocessing and optimized Tesseract settings.
#     Better quality for medical documents.
#     """
    
#     # Step 1: Preprocess image
#     processed = preprocess_image_for_ocr(image)
    
#     # Step 2: OCR with optimized Tesseract config
#     # PSM 3 = Auto with OSD (better for mixed content)
#     # OEM 3 = LSTM neural network
#     text = pytesseract.image_to_string(
#         processed,
#         config="""
#             --oem 3
#             --psm 3
#             -c tesseract_create_pdf=0
#         """
#     )
    
#     return normalize_text(text)


# def get_ocr_confidence(image: Image.Image) -> dict:
#     """
#     Get Tesseract confidence scores for quality assessment.
#     Helps identify when OCR quality is poor.
#     """
#     processed = preprocess_image_for_ocr(image)
    
#     data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT)
    
#     confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
    
#     return {
#         'avg_confidence': round(sum(confidences) / len(confidences), 2) if confidences else 0,
#         'min_confidence': min(confidences) if confidences else 0,
#         'high_confidence_ratio': round(len([c for c in confidences if c >= 80]) / len(confidences) * 100, 2) if confidences else 0,
#         'total_words': len(confidences)
#     }


# # ---------------- DIGITAL PAGE VALIDATION ----------------
# def is_valid_digital(text: str) -> bool:
#     if not text:
#         return False

#     words = text.split()
#     if len(words) < 30:
#         return False

#     # check readable ratio
#     alpha_ratio = sum(c.isalpha() for c in text) / max(len(text), 1)

#     return alpha_ratio > 0.6


# # ---------------- DIGITAL PDF EXTRACT ----------------
# def extract_digital_text_page(page) -> str:
#     try:
#         return normalize_text(page.get_text())
#     except:
#         return ""


# # ---------------- SCANNED PAGE OCR ----------------
# def ocr_pdf_page(page) -> str:
#     """Extract text from a single PDF page using high-quality OCR"""
#     # Render at 300 DPI for better quality
#     pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), alpha=False)
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#     return ocr_image(img)


# # ---------------- HYBRID PDF PROCESSOR ----------------
# def extract_pdf_hybrid(pdf_path: str) -> str:
#     doc = fitz.open(pdf_path)

#     final_text = []

#     for page_num in range(len(doc)):
#         page = doc.load_page(page_num)

#         # Step 1: digital extraction
#         digital_text = extract_digital_text_page(page)

#         # Step 2: decide
#         if is_valid_digital(digital_text):
#             final_text.append(digital_text)
#         else:
#             try:
#                 ocr_text = ocr_pdf_page(page)
#                 final_text.append(ocr_text)
#             except Exception as e:
#                 print(f"⚠️ OCR failed on page {page_num}: {e}")

#     return normalize_text("\n".join(final_text))


# # ---------------- IMAGE PROCESSOR ----------------
# def extract_image_text(file_path: str) -> str:
#     image = Image.open(file_path)
#     return ocr_image(image)


# # ---------------- MAIN ENTRY FUNCTION ----------------
# def extract_text(file_path: str) -> str:
#     ext = os.path.splitext(file_path)[1].lower()

#     # ---------------- IMAGE ----------------
#     if ext in [".png", ".jpg", ".jpeg"]:
#         print("📷 Processing IMAGE OCR...")
#         return extract_image_text(file_path)

#     # ---------------- PDF ----------------
#     elif ext == ".pdf":
#         print("📄 Processing HYBRID PDF extraction...")
#         return extract_pdf_hybrid(file_path)

#     # ---------------- INVALID ----------------
#     else:
#         raise ValueError("Unsupported file type")


# import fitz
# import cv2
# import numpy as np

# from PIL import Image
# from paddleocr import PaddleOCR

# ocr = PaddleOCR(
#     use_angle_cls=True,
#     lang='en'
# )

# def preprocess_image(pil_image):

#     img = np.array(pil_image)

#     gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

#     # CLAHE enhancement
#     clahe = cv2.createCLAHE(
#         clipLimit=2.0,
#         tileGridSize=(8, 8)
#     )

#     enhanced = clahe.apply(gray)

#     # adaptive threshold
#     thresh = cv2.adaptiveThreshold(
#         enhanced,
#         255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY,
#         11,
#         2
#     )

#     return thresh
# def ocr_image(image):

#     processed = preprocess_image(image)

#     result = ocr.ocr(processed)

#     lines = []

#     for block in result:

#         if block is None:
#             continue

#         for line in block:

#             text = line[1][0]

#             lines.append(text)

#     return " ".join(lines)

# def extract_digital_text(page):

#     try:
#         return page.get_text().strip()
#     except:
#         return ""
    
# def is_valid_text(text):

#     if not text:
#         return False

#     if len(text.split()) < 30:
#         return False

#     return True

# def ocr_page(page):

#     pix = page.get_pixmap(dpi=300)

#     img = Image.frombytes(
#         "RGB",
#         [pix.width, pix.height],
#         pix.samples
#     )

#     return ocr_image(img)


# def extract_text(pdf_path):

#     doc = fitz.open(pdf_path)

#     final_text = []

#     for page in doc:

#         digital_text = extract_digital_text(page)

#         if is_valid_text(digital_text):
#             final_text.append(digital_text)

#         else:
#             ocr_text = ocr_page(page)
#             final_text.append(ocr_text)

#     return "\n".join(final_text)

# import fitz
# import cv2
# import numpy as np
# import pytesseract

# from PIL import Image
# from paddleocr import PaddleOCR


# # =====================================
# # TESSERACT CONFIG
# # =====================================

# pytesseract.pytesseract.tesseract_cmd = (
#     r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# )


# # =====================================
# # PADDLE OCR
# # =====================================

# paddle_ocr = PaddleOCR(
#     use_angle_cls=True,
#     lang='en',
#     show_log=False
# )


# # =====================================
# # LIGHT PREPROCESSING
# # =====================================

# def preprocess_image(pil_image):

#     # convert to numpy
#     img = np.array(pil_image)

#     # grayscale only
#     gray = cv2.cvtColor(
#         img,
#         cv2.COLOR_RGB2GRAY
#     )

#     # resize for better OCR
#     resized = cv2.resize(
#         gray,
#         None,
#         fx=2,
#         fy=2,
#         interpolation=cv2.INTER_CUBIC
#     )

#     # mild denoise only
#     denoised = cv2.GaussianBlur(
#         resized,
#         (3, 3),
#         0
#     )

#     return denoised


# # =====================================
# # TESSERACT OCR
# # Better for numeric precision
# # =====================================

# def tesseract_ocr(image):

#     text = pytesseract.image_to_string(
#         image,
#         config="--oem 3 --psm 6"
#     )

#     return text


# # =====================================
# # PADDLE OCR
# # Better for labels/text
# # =====================================

# def paddle_text_ocr(image):

#     result = paddle_ocr.ocr(image)

#     lines = []

#     for block in result:

#         if block is None:
#             continue

#         for line in block:

#             text = line[1][0]

#             lines.append(text)

#     return " ".join(lines)


# # =====================================
# # HYBRID OCR
# # Merge both outputs
# # =====================================

# def hybrid_ocr(image):

#     processed = preprocess_image(image)

#     # Tesseract result
#     tess_text = tesseract_ocr(processed)

#     # Paddle result
#     paddle_text = paddle_text_ocr(processed)

#     # Choose longer/better text
#     if len(paddle_text) > len(tess_text):
#         return paddle_text

#     return tess_text


# # =====================================
# # DIGITAL PDF EXTRACTION
# # =====================================

# def extract_digital_text(page):

#     try:
#         return page.get_text().strip()

#     except:
#         return ""


# # =====================================
# # CHECK IF PAGE IS DIGITAL
# # =====================================

# def is_valid_text(text):

#     if not text:
#         return False

#     words = text.split()

#     if len(words) < 30:
#         return False

#     return True


# # =====================================
# # OCR PAGE
# # =====================================

# def ocr_page(page):

#     pix = page.get_pixmap(dpi=300)

#     img = Image.frombytes(
#         "RGB",
#         [pix.width, pix.height],
#         pix.samples
#     )

#     return hybrid_ocr(img)


# # =====================================
# # PDF EXTRACTION
# # =====================================

# def extract_text(pdf_path):

#     doc = fitz.open(pdf_path)

#     final_text = []

#     for page in doc:

#         # Try digital extraction first
#         digital_text = extract_digital_text(page)

#         # Use digital text if valid
#         if is_valid_text(digital_text):

#             final_text.append(digital_text)

#         else:

#             # OCR fallback
#             ocr_text = ocr_page(page)

#             final_text.append(ocr_text)

#     return "\n".join(final_text)

# OCRHandling/ocr_service.py
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

# 🔧 Windows Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def normalize_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.split())

def preprocess_image_for_ocr(image: Image.Image) -> Image.Image:
    """Safely scales image and improves clarity to maximize Tesseract parsing rates."""
    img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Smart conditional scaling: Only upscale if the image is actually tiny/low-res
    h_orig, w_orig = img_cv.shape[:2]
    if w_orig < 1500:
        scale_factor = 2.0
        img_cv = cv2.resize(img_cv, (int(w_orig * scale_factor), int(h_orig * scale_factor)), interpolation=cv2.INTER_CUBIC)
    
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=10, templateWindowSize=7, searchWindowSize=21)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)
    
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return Image.fromarray(binary)

def ocr_image(image: Image.Image) -> str:
    try:
        processed = preprocess_image_for_ocr(image)
        text = pytesseract.image_to_string(
            processed,
            config="--oem 3 --psm 3"
        )
        return normalize_text(text)
    except Exception as e:
        print(f"Image text processing parsing fault: {e}")
        return ""

def is_valid_digital(text: str) -> bool:
    if not text or len(text.split()) < 30:
        return False
    return (sum(c.isalpha() for c in text) / max(len(text), 1)) > 0.6

def extract_digital_text_page(page) -> str:
    try:
        return normalize_text(page.get_text())
    except:
        return ""

def ocr_pdf_page(page) -> str:
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False) # Optimized scale factor matrix
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return ocr_image(img)

def extract_pdf_hybrid(pdf_path: str) -> str:
    final_text = []
    with fitz.open(pdf_path) as doc:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            digital_text = extract_digital_text_page(page)
            
            if is_valid_digital(digital_text):
                final_text.append(digital_text)
            else:
                try:
                    final_text.append(ocr_pdf_page(page))
                except Exception as e:
                    print(f"⚠️ OCR failed on page {page_num}: {e}")
                    
    return normalize_text("\n".join(final_text))

# MATCH THE EXACT ROUTE FUNCTION NAME REQUIRED BY YOUR ENHANCED PIPELINE
def extract_text(file_path: str) -> str:
    """Unified entry target file path routing engine."""
    if not os.path.exists(file_path):
        return ""
        
    ext = os.path.splitext(file_path)[1].lower()
    if ext in [".png", ".jpg", ".jpeg"]:
        return ocr_image(Image.open(file_path))
    elif ext == ".pdf":
        return extract_pdf_hybrid(file_path)
    else:
        raise ValueError("Unsupported asset target format passed.")