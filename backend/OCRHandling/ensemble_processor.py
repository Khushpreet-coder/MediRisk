# """
# Ensemble OCR + LLM Module for High-Accuracy Medical Text Extraction

# Combines multiple OCR engines and LLM models for improved accuracy
# and confidence scoring in medical report processing.

# Architecture:
# - Multi-Engine OCR: Tesseract + EasyOCR
# - Ensemble LLMs: Groq models for validation
# - Confidence Voting: Reconcile differences
# - Error Correction: Fix inconsistencies
# """

# import os
# import json
# import logging
# from typing import Dict, List, Tuple, Optional
# from dataclasses import dataclass
# from collections import Counter
# import re

# import easyocr
# import pytesseract
# from PIL import Image
# from groq import Groq
# from dotenv import load_dotenv

# logger = logging.getLogger(__name__)
# load_dotenv()


# # =====================================
# # DATA CLASSES
# # =====================================


# @dataclass
# class ExtractedTest:
#     """Represents a single medical test result."""
#     test_name: str
#     value: str
#     unit: str = ""
#     reference_range: str = ""
#     status: str = ""
#     confidence: float = 0.0
#     source: str = "unknown"  # ocr, llm, ensemble


# @dataclass
# class EnsembleResult:
#     """Result from ensemble processing."""
#     tests: List[ExtractedTest]
#     avg_confidence: float
#     total_agreement: float
#     method: str
#     warnings: List[str] = None

#     def __post_init__(self):
#         if self.warnings is None:
#             self.warnings = []


# # =====================================
# # MULTI-ENGINE OCR
# # =====================================


# class MultiEngineOCR:
#     """Combines multiple OCR engines for better accuracy."""

#     def __init__(self):
#         """Initialize OCR engines."""
#         self.tesseract_available = self._check_tesseract()
#         self.easyocr_reader = None
        
#         # Initialize EasyOCR if available
#         try:
#             logger.info("Initializing EasyOCR reader...")
#             self.easyocr_reader = easyocr.Reader(['en'], gpu=False)
#         except Exception as e:
#             logger.warning(f"EasyOCR initialization failed: {e}")

#     @staticmethod
#     def _check_tesseract() -> bool:
#         """Check if Tesseract is available."""
#         try:
#             pytesseract.get_tesseract_version()
#             return True
#         except:
#             return False

#     def ocr_tesseract(self, image: Image.Image) -> Tuple[str, float]:
#         """
#         Extract text using Tesseract.

#         Returns:
#             Tuple of (text, confidence_score)
#         """
#         if not self.tesseract_available:
#             return "", 0.0

#         try:
#             text = pytesseract.image_to_string(
#                 image,
#                 config="--oem 3 --psm 3"
#             )

#             # Get confidence scores
#             data = pytesseract.image_to_data(
#                 image, output_type=pytesseract.Output.DICT
#             )
#             confidences = [int(c) for c in data['conf'] if int(c) > 0]
#             avg_confidence = sum(confidences) / len(confidences) if confidences else 0

#             return text.strip(), avg_confidence / 100

#         except Exception as e:
#             logger.error(f"Tesseract OCR failed: {e}")
#             return "", 0.0

#     def ocr_easyocr(self, image: Image.Image) -> Tuple[str, float]:
#         """
#         Extract text using EasyOCR.

#         Returns:
#             Tuple of (text, confidence_score)
#         """
#         if not self.easyocr_reader:
#             return "", 0.0

#         try:
#             results = self.easyocr_reader.readtext(image, detail=1)
            
#             if not results:
#                 return "", 0.0

#             # Extract text and calculate average confidence
#             texts = [item[1] for item in results]
#             confidences = [item[2] for item in results]

#             text = "\n".join(texts)
#             avg_confidence = sum(confidences) / len(confidences) if confidences else 0

#             return text.strip(), avg_confidence

#         except Exception as e:
#             logger.error(f"EasyOCR failed: {e}")
#             return "", 0.0

#     def extract_ensemble(self, image: Image.Image) -> Tuple[str, float]:
#         """
#         Extract text using both engines and return best result.

#         Returns:
#             Tuple of (best_text, confidence)
#         """
#         tesseract_text, tesseract_conf = self.ocr_tesseract(image)
#         easyocr_text, easyocr_conf = self.ocr_easyocr(image)

#         logger.info(
#             f"Tesseract confidence: {tesseract_conf:.2%}, "
#             f"EasyOCR confidence: {easyocr_conf:.2%}"
#         )

#         # Use highest confidence result
#         if easyocr_conf > tesseract_conf:
#             return easyocr_text, easyocr_conf
#         else:
#             return tesseract_text, tesseract_conf


# # =====================================
# # ENSEMBLE LLM VERIFICATION
# # =====================================


# class EnsembleLLMValidator:
#     """Validates and reconciles extracted data using multiple LLM models."""

#     def __init__(self):
#         """Initialize LLM clients."""
#         self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#         self.models = [
#             "gemma-7b-it",  # Primary model
#             "llama3-8b-8192",  # Secondary model
#         ]

#     def validate_with_multiple_models(self, text: str) -> List[Dict]:
#         """
#         Parse medical report with multiple LLM models and return consensus results.

#         Args:
#             text: Cleaned OCR text

#         Returns:
#             List of extracted tests with confidence scores
#         """
#         results_by_model = []

#         for model in self.models:
#             try:
#                 logger.info(f"Parsing with model: {model}")
#                 result = self._parse_with_model(text, model)
#                 results_by_model.append(result)
#             except Exception as e:
#                 logger.error(f"Model {model} parsing failed: {e}")
#                 continue

#         if not results_by_model:
#             return []

#         # Reconcile results
#         return self._reconcile_results(results_by_model)

#     def _parse_with_model(self, text: str, model: str) -> Dict:
#         """Parse text with specific LLM model."""
#         prompt = f"""
# You are a medical report extraction expert. Extract ALL laboratory tests with status.

# RULES:
# 1. Output ONLY valid JSON
# 2. Extract ALL tests from the report
# 3. Calculate status for every test:
#    - Compare value to reference range
#    - If value < min → "Low"
#    - If value > max → "High"
#    - If within range → "Normal"
#    - If no range → ""

# OUTPUT FORMAT:
# {{
#   "tests": [
#     {{
#       "test_name": "string",
#       "value": "string or number",
#       "unit": "string",
#       "reference_range": "string",
#       "status": "Low/High/Normal/Positive/Negative/Reactive/Critical"
#     }}
#   ]
# }}

# MEDICAL REPORT:
# {text}
# """

#         response = self.groq_client.chat.completions.create(
#             model=model,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0
#         )

#         output = response.choices[0].message.content
#         output = output.replace("```json", "").replace("```", "").strip()

#         try:
#             return json.loads(output)
#         except json.JSONDecodeError:
#             logger.error(f"Failed to parse {model} response as JSON")
#             return {"tests": []}

#     def _reconcile_results(self, results: List[Dict]) -> List[Dict]:
#         """
#         Reconcile results from multiple models using voting.

#         Args:
#             results: List of parsed results from different models

#         Returns:
#             Reconciled test results with confidence scores
#         """
#         if not results:
#             return []

#         # Group tests by name
#         tests_by_name = {}

#         for result in results:
#             for test in result.get("tests", []):
#                 name = test.get("test_name", "").strip().lower()
#                 if not name:
#                     continue

#                 if name not in tests_by_name:
#                     tests_by_name[name] = []

#                 tests_by_name[name].append(test)

#         # Reconcile each test group
#         reconciled = []

#         for test_name, test_variants in tests_by_name.items():
#             reconciled_test = self._reconcile_test_variants(test_name, test_variants)
#             reconciled.append(reconciled_test)

#         return reconciled

#     def _reconcile_test_variants(self, test_name: str, variants: List[Dict]) -> Dict:
#         """Reconcile different versions of the same test."""
#         # Vote on values
#         values = [v.get("value", "") for v in variants]
#         value_votes = Counter(values)
#         best_value = value_votes.most_common(1)[0][0] if value_votes else ""

#         # Vote on units
#         units = [v.get("unit", "") for v in variants]
#         unit_votes = Counter(units)
#         best_unit = unit_votes.most_common(1)[0][0] if unit_votes else ""

#         # Vote on reference ranges
#         ranges = [v.get("reference_range", "") for v in variants]
#         range_votes = Counter(ranges)
#         best_range = range_votes.most_common(1)[0][0] if range_votes else ""

#         # Vote on status
#         statuses = [v.get("status", "") for v in variants]
#         status_votes = Counter(statuses)
#         best_status = status_votes.most_common(1)[0][0] if status_votes else ""

#         # Calculate confidence (agreement ratio)
#         confidence = value_votes[best_value] / len(variants) if variants else 0

#         return {
#             "test_name": test_name.title(),
#             "value": best_value,
#             "unit": best_unit,
#             "reference_range": best_range,
#             "status": best_status,
#             "confidence": confidence,
#             "agreement": len([v for v in variants if v.get("value") == best_value]) / len(variants)
#         }


# # =====================================
# # FULL ENSEMBLE PIPELINE
# # =====================================


# class OCRLLMEnsemble:
#     """
#     Complete ensemble pipeline combining OCR and LLM validation.

#     Pipeline:
#     1. Multi-engine OCR (Tesseract + EasyOCR)
#     2. Ensemble LLM validation (multiple models)
#     3. Confidence scoring
#     4. Result reconciliation
#     """

#     def __init__(self):
#         """Initialize ensemble components."""
#         self.ocr = MultiEngineOCR()
#         self.llm_validator = EnsembleLLMValidator()

#     def process_image(self, image: Image.Image) -> EnsembleResult:
#         """
#         Process image with full ensemble pipeline.

#         Args:
#             image: PIL Image object

#         Returns:
#             EnsembleResult with tests and confidence metrics
#         """
#         logger.info("Starting ensemble OCR processing...")

#         # Step 1: Multi-engine OCR
#         ocr_text, ocr_confidence = self.ocr.extract_ensemble(image)

#         if not ocr_text:
#             return EnsembleResult(
#                 tests=[],
#                 avg_confidence=0.0,
#                 total_agreement=0.0,
#                 method="ensemble",
#                 warnings=["OCR extraction failed"]
#             )

#         logger.info(f"OCR extraction confidence: {ocr_confidence:.2%}")

#         # Step 2: Ensemble LLM validation
#         tests = self.llm_validator.validate_with_multiple_models(ocr_text)

#         if not tests:
#             return EnsembleResult(
#                 tests=[],
#                 avg_confidence=0.0,
#                 total_agreement=0.0,
#                 method="ensemble",
#                 warnings=["LLM validation failed"]
#             )

#         # Step 3: Calculate metrics
#         avg_confidence = sum(t.get("confidence", 0) for t in tests) / len(tests) if tests else 0
#         avg_agreement = sum(t.get("agreement", 0) for t in tests) / len(tests) if tests else 0

#         logger.info(f"Ensemble average confidence: {avg_confidence:.2%}")
#         logger.info(f"Ensemble average agreement: {avg_agreement:.2%}")

#         return EnsembleResult(
#             tests=tests,
#             avg_confidence=avg_confidence,
#             total_agreement=avg_agreement,
#             method="ensemble_ocr_llm"
#         )


# # =====================================
# # UTILITY FUNCTIONS
# # =====================================


# def merge_ensemble_results(results: List[EnsembleResult]) -> Dict:
#     """
#     Merge multiple ensemble results into single output.

#     Args:
#         results: List of EnsembleResult objects

#     Returns:
#         Merged result dictionary
#     """
#     all_tests = []
#     total_confidence = 0
#     total_agreement = 0

#     for result in results:
#         all_tests.extend(result.tests)
#         total_confidence += result.avg_confidence
#         total_agreement += result.total_agreement

#     avg_confidence = total_confidence / len(results) if results else 0
#     avg_agreement = total_agreement / len(results) if results else 0

#     return {
#         "tests": all_tests,
#         "metrics": {
#             "avg_confidence": round(avg_confidence, 3),
#             "avg_agreement": round(avg_agreement, 3),
#             "total_tests": len(all_tests),
#             "method": "ensemble_ocr_llm"
#         }
#     }



# """
# Ensemble OCR + Hugging Face LLM Processing Module
# Replaces Groq with Hugging Face Transformers
# """

# import os
# import json
# import logging
# from typing import Dict, List, Tuple
# from dataclasses import dataclass
# from collections import Counter

# import easyocr
# import pytesseract
# from PIL import Image

# from transformers import pipeline

# logger = logging.getLogger(__name__)


# # =====================================
# # DATA CLASSES
# # =====================================

# @dataclass
# class ExtractedTest:
#     test_name: str
#     value: str
#     unit: str = ""
#     reference_range: str = ""
#     status: str = ""
#     confidence: float = 0.0
#     source: str = "hf"


# @dataclass
# class EnsembleResult:
#     tests: List[Dict]
#     avg_confidence: float
#     total_agreement: float
#     method: str
#     warnings: List[str] = None

#     def __post_init__(self):
#         if self.warnings is None:
#             self.warnings = []


# # =====================================
# # MULTI OCR ENGINE
# # =====================================

# class MultiEngineOCR:
#     def __init__(self):
#         self.tesseract_available = self._check_tesseract()

#         try:
#             self.easyocr_reader = easyocr.Reader(['en'], gpu=False)
#         except Exception as e:
#             logger.warning(f"EasyOCR init failed: {e}")
#             self.easyocr_reader = None

#     def _check_tesseract(self):
#         try:
#             pytesseract.get_tesseract_version()
#             return True
#         except:
#             return False

#     def ocr_tesseract(self, image):
#         if not self.tesseract_available:
#             return "", 0.0

#         text = pytesseract.image_to_string(image, config="--oem 3 --psm 3")
#         return text.strip(), 0.7  # fallback confidence

#     def ocr_easyocr(self, image):
#         if not self.easyocr_reader:
#             return "", 0.0

#         results = self.easyocr_reader.readtext(image)

#         if not results:
#             return "", 0.0

#         texts = [r[1] for r in results]
#         confs = [r[2] for r in results]

#         return "\n".join(texts), sum(confs) / len(confs)

#     def extract(self, image):
#         t_text, t_conf = self.ocr_tesseract(image)
#         e_text, e_conf = self.ocr_easyocr(image)

#         if e_conf > t_conf:
#             return e_text, e_conf
#         return t_text, t_conf


# # =====================================
# # HUGGING FACE LLM PROCESSOR
# # =====================================

# class HFLLMProcessor:
#     def __init__(self):
#         logger.info("Loading Hugging Face models...")

#         # 🧠 Main extraction model
#         self.parser = pipeline(
#     "text2text-generation",
#     model="google/flan-t5-base",
#     framework="pt",
#     device=-1
# )

# self.small_parser = pipeline(
#     "text2text-generation",
#     model="google/flan-t5-small",
#     framework="pt",
#     device=-1
# )

# self.summarizer = pipeline(
#     "text2text-generation",
#     model="google/flan-t5-base",
#     framework="pt",
#     device=-1
# )

#     def parse_tests(self, text: str) -> Dict:
#         prompt = f"""
# Extract medical tests from the text.

# Return ONLY valid JSON:
# {{
#   "tests": [
#     {{
#       "test_name": "",
#       "value": "",
#       "unit": "",
#       "reference_range": "",
#       "status": ""
#     }}
#   ]
# }}

# TEXT:
# {text}
# """

#         try:
#             result = self.parser(prompt)
#             output = result[0]["generated_text"]

#             output = output.replace("```json", "").replace("```", "").strip()

#             return json.loads(output)

#         except Exception as e:
#             logger.warning(f"Primary model failed: {e}")

#             # fallback
#             try:
#                 result = self.small_parser(prompt)
#                 output = result[0]["generated_text"]
#                 output = output.replace("```json", "").replace("```", "").strip()
#                 return json.loads(output)
#             except:
#                 return {"tests": []}

#     def generate_summary(self, text: str) -> str:
#         prompt = f"""
# Summarize this medical report in simple language:

# {text}
# """

#         try:
#             result = self.summarizer(prompt)
#             return result[0]["generated_text"]
#         except Exception as e:
#             logger.error(f"Summary failed: {e}")
#             return "Summary not available"


# # =====================================
# # SIMPLE ENSEMBLE LOGIC (NO GROQ)
# # =====================================

# class SimpleEnsemble:
#     def reconcile(self, results: List[Dict]) -> List[Dict]:
#         """Merge duplicate test entries using voting"""

#         test_map = {}

#         for result in results:
#             for test in result.get("tests", []):
#                 name = test.get("test_name", "").lower().strip()
#                 if not name:
#                     continue

#                 if name not in test_map:
#                     test_map[name] = []

#                 test_map[name].append(test)

#         final = []

#         for name, variants in test_map.items():
#             values = [v.get("value", "") for v in variants]
#             value = Counter(values).most_common(1)[0][0]

#             units = [v.get("unit", "") for v in variants]
#             unit = Counter(units).most_common(1)[0][0]

#             ranges = [v.get("reference_range", "") for v in variants]
#             ref = Counter(ranges).most_common(1)[0][0]

#             statuses = [v.get("status", "") for v in variants]
#             status = Counter(statuses).most_common(1)[0][0]

#             final.append({
#                 "test_name": name.title(),
#                 "value": value,
#                 "unit": unit,
#                 "reference_range": ref,
#                 "status": status,
#                 "confidence": len(variants) / max(len(variants), 1)
#             })

#         return final


# # =====================================
# # MAIN PIPELINE
# # =====================================

# class OCRHFEnsemblePipeline:
#     def __init__(self):
#         self.ocr = MultiEngineOCR()
#         self.llm = HFLLMProcessor()
#         self.ensemble = SimpleEnsemble()

#     def process_image(self, image) -> EnsembleResult:
#         logger.info("Starting HF pipeline...")

#         # 1. OCR
#         text, confidence = self.ocr.extract(image)

#         if not text:
#             return EnsembleResult(
#                 tests=[],
#                 avg_confidence=0.0,
#                 total_agreement=0.0,
#                 method="hf_pipeline",
#                 warnings=["OCR failed"]
#             )

#         # 2. LLM parsing (single model, stable)
#         parsed = self.llm.parse_tests(text)

#         tests = parsed.get("tests", [])

#         if not tests:
#             return EnsembleResult(
#                 tests=[],
#                 avg_confidence=0.0,
#                 total_agreement=0.0,
#                 method="hf_pipeline",
#                 warnings=["LLM parsing failed"]
#             )

#         # 3. Fake ensemble (kept for compatibility)
#         final_tests = self.ensemble.reconcile([parsed])

#         avg_conf = 0.8 if final_tests else 0.0

#         return EnsembleResult(
#             tests=final_tests,
#             avg_confidence=avg_conf,
#             total_agreement=1.0,
#             method="huggingface_pipeline"
#         )


# # =====================================
# # HELPER
# # =====================================

# def merge_results(results: List[EnsembleResult]) -> Dict:
#     all_tests = []

#     for r in results:
#         all_tests.extend(r.tests)

#     return {
#         "tests": all_tests,
#         "total": len(all_tests),
#         "method": "hf_pipeline"
#     }

# """
# Ensemble OCR + Hugging Face LLM Processing Module
# Replaces Groq with Hugging Face Transformers
# """

# import os
# import json
# import logging
# from typing import Dict, List, Tuple
# from dataclasses import dataclass
# from collections import Counter


# import easyocr
# import pytesseract
# from PIL import Image

# from transformers import pipeline

# logger = logging.getLogger(__name__)


# # =====================================
# # DATA CLASSES
# # =====================================

# @dataclass
# class ExtractedTest:
#     test_name: str
#     value: str
#     unit: str = ""
#     reference_range: str = ""
#     status: str = ""
#     confidence: float = 0.0
#     source: str = "hf"


# @dataclass
# class EnsembleResult:
#     tests: List[Dict]
#     avg_confidence: float
#     total_agreement: float
#     method: str
#     warnings: List[str] = None

#     def __post_init__(self):
#         if self.warnings is None:
#             self.warnings = []


# # =====================================
# # MULTI OCR ENGINE
# # =====================================

# class MultiEngineOCR:
#     def __init__(self):
#         self.tesseract_available = self._check_tesseract()

#         try:
#             self.easyocr_reader = easyocr.Reader(['en'], gpu=False)
#         except Exception as e:
#             logger.warning(f"EasyOCR init failed: {e}")
#             self.easyocr_reader = None

#     def _check_tesseract(self):
#         try:
#             pytesseract.get_tesseract_version()
#             return True
#         except:
#             return False

#     def ocr_tesseract(self, image):
#         if not self.tesseract_available:
#             return "", 0.0

#         text = pytesseract.image_to_string(image, config="--oem 3 --psm 3")
#         return text.strip(), 0.7

#     def ocr_easyocr(self, image):
#         if not self.easyocr_reader:
#             return "", 0.0

#         results = self.easyocr_reader.readtext(image)

#         if not results:
#             return "", 0.0

#         texts = [r[1] for r in results]
#         confs = [r[2] for r in results]

#         return "\n".join(texts), sum(confs) / len(confs)

#     def extract(self, image):
#         t_text, t_conf = self.ocr_tesseract(image)
#         e_text, e_conf = self.ocr_easyocr(image)

#         if e_conf > t_conf:
#             return e_text, e_conf
#         return t_text, t_conf


# # =====================================
# # HUGGING FACE LLM PROCESSOR
# # =====================================
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# import torch
# import json
# import logging

# logger = logging.getLogger(__name__)


# class HFLLMProcessor:
#     def __init__(self):
#         logger.info("Loading Hugging Face models...")

#         self.device = "cpu"

#         # Main model
#         self.model_name = "google/flan-t5-base"

#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

#         self.model = AutoModelForSeq2SeqLM.from_pretrained(
#             self.model_name
#         ).to(self.device)

#     def generate(self, prompt, max_new_tokens=256):

#         inputs = self.tokenizer(
#             prompt,
#             return_tensors="pt",
#             truncation=True,
#             max_length=512
#         ).to(self.device)

#         outputs = self.model.generate(
#             **inputs,
#             max_new_tokens=max_new_tokens
#         )

#         return self.tokenizer.decode(
#             outputs[0],
#             skip_special_tokens=True
#         )

#     def parse_tests(self, text: str):

#     prompt = f"""
# Extract medical tests from the report.

# Return ONLY valid JSON in this exact format:

# {{
#   "tests": [
#     {{
#       "test_name": "",
#       "value": "",
#       "unit": "",
#       "reference_range": "",
#       "status": ""
#     }}
#   ]
# }}

# REPORT:
# {text[:3000]}
# """

#     try:
#         output = self.generate(prompt)

#         print("HF RAW OUTPUT:\n", output)

#         output = output.replace("```json", "")
#         output = output.replace("```", "")
#         output = output.strip()

#         # find JSON block safely
#         start = output.find("{")
#         end = output.rfind("}")

#         if start != -1 and end != -1:
#             output = output[start:end + 1]

#         parsed = json.loads(output)

#         if "tests" not in parsed:
#             parsed["tests"] = []

#         return parsed

#     except Exception as e:
#         logger.error(f"Parsing failed: {e}")

#         return {
#             "tests": []
#         }
       

#     def generate_summary(self, text: str):

#         prompt = f"""
# Summarize this medical report in simple language:

# {text}
# """

#         try:
#             return self.generate(prompt, max_new_tokens=150)

#         except Exception as e:
#             logger.error(f"Summary failed: {e}")
#             return "Summary not available"

#     def llm_validator(self, data):
#         return data


       


# # =====================================
# # SIMPLE ENSEMBLE LOGIC (NO GROQ)
# # =====================================

# class SimpleEnsemble:
#     def reconcile(self, results: List[Dict]) -> List[Dict]:
#         """Merge duplicate test entries using voting"""

#         test_map = {}

#         for result in results:
#             for test in result.get("tests", []):
#                 name = test.get("test_name", "").lower().strip()
#                 if not name:
#                     continue

#                 test_map.setdefault(name, []).append(test)

#         final = []

#         for name, variants in test_map.items():
#             values = [v.get("value", "") for v in variants]
#             value = Counter(values).most_common(1)[0][0]

#             units = [v.get("unit", "") for v in variants]
#             unit = Counter(units).most_common(1)[0][0]

#             ranges = [v.get("reference_range", "") for v in variants]
#             ref = Counter(ranges).most_common(1)[0][0]

#             statuses = [v.get("status", "") for v in variants]
#             status = Counter(statuses).most_common(1)[0][0]

#             final.append({
#                 "test_name": name.title(),
#                 "value": value,
#                 "unit": unit,
#                 "reference_range": ref,
#                 "status": status,
#                 "confidence": len(variants)
#             })

#         return final


# # =====================================
# # MAIN PIPELINE
# # =====================================

# class OCRHFEnsemblePipeline:
#     def __init__(self):
#         self.ocr = MultiEngineOCR()
#         self.llm = HFLLMProcessor()
#         self.ensemble = SimpleEnsemble()

#     def process_image(self, image) -> EnsembleResult:
#         logger.info("Starting HF pipeline...")

#         text, confidence = self.ocr.extract(image)

#         if not text:
#             return EnsembleResult(
#                 tests=[],
#                 avg_confidence=0.0,
#                 total_agreement=0.0,
#                 method="hf_pipeline",
#                 warnings=["OCR failed"]
#             )

#         parsed = self.llm.parse_tests(text)
#         tests = parsed.get("tests", [])

#         if not tests:
#             return EnsembleResult(
#                 tests=[],
#                 avg_confidence=0.0,
#                 total_agreement=0.0,
#                 method="hf_pipeline",
#                 warnings=["LLM parsing failed"]
#             )

#         final_tests = self.ensemble.reconcile([parsed])

#         return EnsembleResult(
#             tests=final_tests,
#             avg_confidence=0.8 if final_tests else 0.0,
#             total_agreement=1.0,
#             method="huggingface_pipeline"
#         )


# # =====================================
# # HELPER
# # =====================================

# def merge_results(results: List[EnsembleResult]) -> Dict:
#     all_tests = []

#     for r in results:
#         all_tests.extend(r.tests)

#     return {
#         "tests": all_tests,
#         "total": len(all_tests),
#         "method": "hf_pipeline"
#     }

# """
# Ensemble OCR + Hugging Face LLM Processing Module
# Replaces Groq with Hugging Face Transformers
# """

# import json
# import logging

# from typing import Dict, List
# from dataclasses import dataclass
# from collections import Counter

# import easyocr
# import pytesseract

# from PIL import Image

# from transformers import (
#     AutoTokenizer,
#     AutoModelForSeq2SeqLM
# )

# logger = logging.getLogger(__name__)


# # =====================================
# # DATA CLASSES
# # =====================================

# @dataclass
# class ExtractedTest:
#     test_name: str
#     value: str
#     unit: str = ""
#     reference_range: str = ""
#     status: str = ""
#     confidence: float = 0.0
#     source: str = "hf"


# @dataclass
# class EnsembleResult:
#     tests: List[Dict]
#     avg_confidence: float
#     total_agreement: float
#     method: str
#     warnings: List[str] = None

#     def __post_init__(self):

#         if self.warnings is None:
#             self.warnings = []


# # =====================================
# # MULTI OCR ENGINE
# # =====================================

# class MultiEngineOCR:

#     def __init__(self):

#         self.tesseract_available = self._check_tesseract()

#         try:
#             self.easyocr_reader = easyocr.Reader(
#                 ['en'],
#                 gpu=False
#             )

#         except Exception as e:

#             logger.warning(f"EasyOCR init failed: {e}")
#             self.easyocr_reader = None

#     def _check_tesseract(self):

#         try:
#             pytesseract.get_tesseract_version()
#             return True

#         except:
#             return False

#     def ocr_tesseract(self, image):

#         if not self.tesseract_available:
#             return "", 0.0

#         text = pytesseract.image_to_string(
#             image,
#             config="--oem 3 --psm 3"
#         )

#         return text.strip(), 0.7

#     def ocr_easyocr(self, image):

#         if not self.easyocr_reader:
#             return "", 0.0

#         results = self.easyocr_reader.readtext(image)

#         if not results:
#             return "", 0.0

#         texts = [r[1] for r in results]
#         confs = [r[2] for r in results]

#         return "\n".join(texts), sum(confs) / len(confs)

#     def extract(self, image):

#         t_text, t_conf = self.ocr_tesseract(image)

#         e_text, e_conf = self.ocr_easyocr(image)

#         if e_conf > t_conf:
#             return e_text, e_conf

#         return t_text, t_conf


# # =====================================
# # HUGGING FACE LLM PROCESSOR
# # =====================================

# class HFLLMProcessor:

#     def __init__(self):

#         logger.info("Loading Hugging Face models...")

#         self.device = "cpu"

#         # Main model
#         self.model_name = "google/flan-t5-base"

#         self.tokenizer = AutoTokenizer.from_pretrained(
#             self.model_name
#         )

#         self.model = AutoModelForSeq2SeqLM.from_pretrained(
#             self.model_name
#         ).to(self.device)

#     # =====================================
#     # GENERATE TEXT
#     # =====================================

#     def generate(self, prompt, max_new_tokens=256):

#         inputs = self.tokenizer(
#             prompt,
#             return_tensors="pt",
#             truncation=True,
#             max_length=512
#         ).to(self.device)

#         outputs = self.model.generate(
#             **inputs,
#             max_new_tokens=max_new_tokens
#         )

#         return self.tokenizer.decode(
#             outputs[0],
#             skip_special_tokens=True
#         )

#     # =====================================
#     # PARSE MEDICAL TESTS
#     # =====================================

#     def parse_tests(self, text: str):

#         prompt = f"""
# Extract medical tests from the report.

# Return ONLY valid JSON in this exact format:

# {{
#   "tests": [
#     {{
#       "test_name": "",
#       "value": "",
#       "unit": "",
#       "reference_range": "",
#       "status": ""
#     }}
#   ]
# }}

# REPORT:
# {text[:3000]}
# """

#         try:

#             output = self.generate(prompt)

#             print("\n==============================")
#             print("HF RAW OUTPUT:")
#             print(output)
#             print("==============================\n")

#             # cleanup
#             output = output.replace("```json", "")
#             output = output.replace("```", "")
#             output = output.strip()

#             # safely extract JSON
#             start = output.find("{")
#             end = output.rfind("}")

#             if start != -1 and end != -1:
#                 output = output[start:end + 1]

#             parsed = json.loads(output)

#             # safety fallback
#             if "tests" not in parsed:
#                 parsed["tests"] = []

#             return parsed

#         except Exception as e:

#             logger.error(f"Parsing failed: {e}")

#             return {
#                 "tests": []
#             }

#     # =====================================
#     # GENERATE SUMMARY
#     # =====================================

#     def generate_summary(self, text: str):

#         prompt = f"""
# Summarize this medical report in simple language.

# REPORT:
# {text[:3000]}
# """

#         try:

#             return self.generate(
#                 prompt,
#                 max_new_tokens=150
#             )

#         except Exception as e:

#             logger.error(f"Summary failed: {e}")

#             return "Summary not available"


# # =====================================
# # SIMPLE ENSEMBLE LOGIC
# # =====================================

# class SimpleEnsemble:

#     def reconcile(self, results: List[Dict]) -> List[Dict]:

#         test_map = {}

#         for result in results:

#             for test in result.get("tests", []):

#                 name = test.get(
#                     "test_name",
#                     ""
#                 ).lower().strip()

#                 if not name:
#                     continue

#                 test_map.setdefault(name, []).append(test)

#         final = []

#         for name, variants in test_map.items():

#             values = [v.get("value", "") for v in variants]
#             value = Counter(values).most_common(1)[0][0]

#             units = [v.get("unit", "") for v in variants]
#             unit = Counter(units).most_common(1)[0][0]

#             ranges = [
#                 v.get("reference_range", "")
#                 for v in variants
#             ]

#             ref = Counter(ranges).most_common(1)[0][0]

#             statuses = [
#                 v.get("status", "")
#                 for v in variants
#             ]

#             status = Counter(statuses).most_common(1)[0][0]

#             final.append({
#                 "test_name": name.title(),
#                 "value": value,
#                 "unit": unit,
#                 "reference_range": ref,
#                 "status": status,
#                 "confidence": len(variants)
#             })

#         return final


# # =====================================
# # MAIN PIPELINE
# # =====================================

# class OCRHFEnsemblePipeline:

#     def __init__(self):

#         self.ocr = MultiEngineOCR()
#         self.llm = HFLLMProcessor()
#         self.ensemble = SimpleEnsemble()

#     def process_image(self, image) -> EnsembleResult:

#         logger.info("Starting HF pipeline...")

#         text, confidence = self.ocr.extract(image)

#         if not text:

#             return EnsembleResult(
#                 tests=[],
#                 avg_confidence=0.0,
#                 total_agreement=0.0,
#                 method="hf_pipeline",
#                 warnings=["OCR failed"]
#             )

#         parsed = self.llm.parse_tests(text)

#         tests = parsed.get("tests", [])

#         if not tests:

#             return EnsembleResult(
#                 tests=[],
#                 avg_confidence=0.0,
#                 total_agreement=0.0,
#                 method="hf_pipeline",
#                 warnings=["LLM parsing failed"]
#             )

#         final_tests = self.ensemble.reconcile([parsed])

#         return EnsembleResult(
#             tests=final_tests,
#             avg_confidence=0.8 if final_tests else 0.0,
#             total_agreement=1.0,
#             method="huggingface_pipeline"
#         )


# # =====================================
# # HELPER
# # =====================================

# def merge_results(results: List[EnsembleResult]) -> Dict:

#     all_tests = []

#     for r in results:
#         all_tests.extend(r.tests)

#     return {
#         "tests": all_tests,
#         "total": len(all_tests),
#         "method": "hf_pipeline"
#     }

# """
# Ensemble OCR + Google Gemini LLM Processing Module
# Replaces Hugging Face Transformers with Gemini API
# """

# import json
# import logging
# from typing import Dict, List
# from dataclasses import dataclass
# from collections import Counter
# import easyocr
# import pytesseract
# from PIL import Image

# # Google GenAI imports
# from google import genai
# from google.genai import types

# logger = logging.getLogger(__name__)


# # =====================================
# # DATA CLASSES
# # =====================================

# @dataclass
# class ExtractedTest:
#     test_name: str
#     value: str
#     unit: str = ""
#     reference_range: str = ""
#     status: str = ""
#     confidence: float = 0.0
#     source: str = "gemini"


# @dataclass
# class EnsembleResult:
#     tests: List[Dict]
#     avg_confidence: float
#     total_agreement: float
#     method: str
#     warnings: List[str] = None

#     def __post_init__(self):
#         if self.warnings is None:
#             self.warnings = []


# # =====================================
# # MULTI OCR ENGINE
# # =====================================

# class MultiEngineOCR:
#     def __init__(self):
#         self.tesseract_available = self._check_tesseract()
#         try:
#             self.easyocr_reader = easyocr.Reader(['en'], gpu=False)
#         except Exception as e:
#             logger.warning(f"EasyOCR init failed: {e}")
#             self.easyocr_reader = None

#     def _check_tesseract(self):
#         try:
#             pytesseract.get_tesseract_version()
#             return True
#         except:
#             return False

#     def ocr_tesseract(self, image):
#         if not self.tesseract_available:
#             return "", 0.0
#         text = pytesseract.image_to_string(image, config="--oem 3 --psm 3")
#         return text.strip(), 0.7

#     def ocr_easyocr(self, image):
#         if not self.easyocr_reader:
#             return "", 0.0
#         results = self.easyocr_reader.readtext(image)
#         if not results:
#             return "", 0.0
#         texts = [r[1] for r in results]
#         confs = [r[2] for r in results]
#         return "\n".join(texts), sum(confs) / len(confs)

#     def extract(self, image):
#         t_text, t_conf = self.ocr_tesseract(image)
#         e_text, e_conf = self.ocr_easyocr(image)
#         if e_conf > t_conf:
#             return e_text, e_conf
#         return t_text, t_conf


# # =====================================
# # GEMINI LLM PROCESSOR
# # =====================================

# class HFLLMProcessor:  # Kept the class name unchanged to avoid breaking downstream file imports
#     def __init__(self):
#         logger.info("Initializing Google Gemini API Client...")
#         try:
#             # Automatically picks up GEMINI_API_KEY from environment variables
#             self.client = genai.Client()
#             self.model_name = "gemini-2.5-flash"
#         except Exception as e:
#             logger.error(f"Failed to initialize Gemini Client: {e}")
#             self.client = None

#     def generate(self, prompt: str, max_new_tokens: int = 256, system_instruction: str = None) -> str:
#         if not self.client:
#             logger.error("Gemini client uninitialized.")
#             return ""

#         try:
#             config = types.GenerateContentConfig(
#                 temperature=0.1,
#                 max_output_tokens=max_new_tokens
#             )
#             if system_instruction:
#                 config.system_instruction = system_instruction

#             response = self.client.models.generate_content(
#                 model=self.model_name,
#                 contents=prompt,
#                 config=config
#             )
#             return response.text.strip() if response.text else ""
#         except Exception as e:
#             logger.error(f"Gemini generation error: {e}")
#             return ""

#     def parse_tests(self, text: str) -> Dict:
#         """
#         Parses raw report strings into structural data schemas.
#         """
#         if not self.client:
#             return {"tests": []}

#         system_prompt = "You are a specialized medical data extractor. Extract laboratory test entities into structured formats."
        
#         prompt = f"""
# Extract medical tests from the following report snippet. 
# Ensure you accurately parse test names, numerical values, units, reference intervals, and status flags (e.g., High, Low, Normal).

# Return ONLY valid JSON in this exact structure:
# {{
#   "tests": [
#     {{
#       "test_name": "Test Name Here",
#       "value": "Value Here",
#       "unit": "Unit Here",
#       "reference_range": "Reference Range Here",
#       "status": "Status Here"
#     }}
#   ]
# }}

# REPORT:
# {text[:4000]}
# """
#         try:
#             output = self.generate(prompt, max_new_tokens=1000, system_instruction=system_prompt)
            
#             # Sanitize block formatting quirks
#             output = output.replace("```json", "").replace("```", "").strip()
            
#             start = output.find("{")
#             end = output.rfind("}")
#             if start != -1 and end != -1:
#                 output = output[start:end + 1]

#             parsed = json.loads(output)
#             if "tests" not in parsed:
#                 parsed["tests"] = []
#             return parsed

#         except Exception as e:
#             logger.error(f"Gemini parsing failed: {e}")
#             return {"tests": []}

#     def generate_summary(self, text: str) -> str:
#         prompt = f"Summarize this medical report in simple, conversational language:\n\nREPORT:\n{text[:4000]}"
#         try:
#             return self.generate(prompt, max_new_tokens=256)
#         except Exception as e:
#             logger.error(f"Summary failed: {e}")
#             return "Summary not available"


# # =====================================
# # SIMPLE ENSEMBLE LOGIC
# # =====================================

# class SimpleEnsemble:
#     def reconcile(self, results: List[Dict]) -> List[Dict]:
#         test_map = {}
#         for result in results:
#             for test in result.get("tests", []):
#                 name = test.get("test_name", "").lower().strip()
#                 if not name:
#                     continue
#                 test_map.setdefault(name, []).append(test)

#         final = []
#         for name, variants in test_map.items():
#             values = [v.get("value", "") for v in variants]
#             value = Counter(values).most_common(1)[0][0]

#             units = [v.get("unit", "") for v in variants]
#             unit = Counter(units).most_common(1)[0][0]

#             ranges = [v.get("reference_range", "") for v in variants]
#             ref = Counter(ranges).most_common(1)[0][0]

#             statuses = [v.get("status", "") for v in variants]
#             status = Counter(statuses).most_common(1)[0][0]

#             final.append({
#                 "test_name": name.title(),
#                 "value": value,
#                 "unit": unit,
#                 "reference_range": ref,
#                 "status": status,
#                 "confidence": len(variants)
#             })
#         return final


# # =====================================
# # MAIN PIPELINE
# # =====================================

# class OCRHFEnsemblePipeline:
#     def __init__(self):
#         self.ocr = MultiEngineOCR()
#         self.llm = HFLLMProcessor()
#         self.ensemble = SimpleEnsemble()

#     def process_image(self, image) -> EnsembleResult:
#         logger.info("Starting Gemini-powered pipeline...")
#         text, confidence = self.ocr.extract(image)

#         if not text:
#             return EnsembleResult(
#                 tests=[], avg_confidence=0.0, total_agreement=0.0,
#                 method="gemini_pipeline", warnings=["OCR failed"]
#             )

#         parsed = self.llm.parse_tests(text)
#         tests = parsed.get("tests", [])

#         if not tests:
#             return EnsembleResult(
#                 tests=[], avg_confidence=0.0, total_agreement=0.0,
#                 method="gemini_pipeline", warnings=["LLM parsing failed"]
#             )

#         final_tests = self.ensemble.reconcile([parsed])
#         return EnsembleResult(
#             tests=final_tests,
#             avg_confidence=0.95 if final_tests else 0.0,
#             total_agreement=1.0,
#             method="gemini_pipeline"
#         )


# def merge_results(results: List[EnsembleResult]) -> Dict:
#     all_tests = []
#     for r in results:
#         all_tests.extend(r.tests)
#     return {
#         "tests": all_tests,
#         "total": len(all_tests),
#         "method": "gemini_pipeline"
#     }


# """
# Lightweight Core Text Processor via Google Gemini
# Removes all complex voting/ensemble overhead.
# """

# import json
# import logging
# import easyocr
# import pytesseract

# from google import genai
# from google.genai import types

# logger = logging.getLogger(__name__)

# class MultiEngineOCR:
#     def __init__(self):
#         self.tesseract_available = self._check_tesseract()
#         try:
#             self.easyocr_reader = easyocr.Reader(['en'], gpu=False)
#         except Exception as e:
#             logger.warning(f"EasyOCR init failed: {e}")
#             self.easyocr_reader = None

#     def _check_tesseract(self):
#         try:
#             pytesseract.get_tesseract_version()
#             return True
#         except:
#             return False

#     def extract(self, image) -> str:
#         """Runs fast multi-engine fallback text extraction."""
#         t_text = ""
#         if self.tesseract_available:
#             try:
#                 t_text = pytesseract.image_to_string(image, config="--oem 3 --psm 3").strip()
#             except Exception as e:
#                 logger.error(f"Tesseract extraction error: {e}")

#         if t_text and len(t_text) > 100:
#             return t_text

#         if self.easyocr_reader:
#             try:
#                 results = self.easyocr_reader.readtext(image)
#                 return "\n".join([r[1] for r in results])
#             except Exception as e:
#                 logger.error(f"EasyOCR extraction error: {e}")

#         return t_text


# class HFLLMProcessor: 
#     """
#     Renamed to maintain downstream import compatibility, 
#     but executing purely via native cloud-based Gemini requests.
#     """
#     def __init__(self):
#         try:
#             self.client = genai.Client()
#             self.model_name = "gemini-2.5-flash"
#         except Exception as e:
#             logger.error(f"Failed to initialize Gemini Client: {e}")
#             self.client = None

#     def generate(self, prompt: str, max_new_tokens: int = 400, system_instruction: str = None) -> str:
#         if not self.client:
#             return ""
#         try:
#             config = types.GenerateContentConfig(
#                 temperature=0.1,
#                 max_output_tokens=max_new_tokens,
#                 system_instruction=system_instruction
#             )
#             response = self.client.models.generate_content(
#                 model=self.model_name,
#                 contents=prompt,
#                 config=config
#             )
#             return response.text.strip() if response.text else ""
#         except Exception as e:
#             logger.error(f"Gemini API Error: {e}")
#             return ""

#     def parse_tests(self, text: str) -> dict:
#         """Direct, structural JSON extraction from raw OCR blocks."""
#         if not self.client:
#             return {"tests": []}

#         system_prompt = "You are a specialized medical lab data parser. Output valid JSON arrays strictly following user structures."
#         prompt = f"""
# Extract medical laboratory tests from this text. Identify test names, values, units, reference intervals, and status flags.

# Return ONLY a valid JSON object matching this structure:
# {{
#   "tests": [
#     {{
#       "test_name": "string",
#       "value": "string",
#       "unit": "string",
#       "reference_range": "string",
#       "status": "string"
#     }}
#   ]
# }}

# REPORT TEXT:
# {text}
# """
#         try:
#             output = self.generate(prompt, max_new_tokens=1500, system_instruction=system_prompt)
#             output = output.replace("```json", "").replace("```", "").strip()
            
#             start = output.find("{")
#             end = output.rfind("}")
#             if start != -1 and end != -1:
#                 output = output[start:end + 1]

#             return json.loads(output)
#         except Exception as e:
#             logger.error(f"JSON Structure parsing failure: {e}")
#             return {"tests": []}

# OCRHandling/ensemble_processor.py
# import json
# import logging
# from google import genai
# from google.genai import types

# logger = logging.getLogger(__name__)

# class HFLLMProcessor: 
#     def __init__(self):
#         try:
#             # Looks automatically for GEMINI_API_KEY inside environmental configs
#             self.client = genai.Client()
#             self.model_name = "gemini-2.5-flash"
#         except Exception as e:
#             logger.error(f"Failed to load structural Gemini client engine instance: {e}")
#             self.client = None

#     def generate(self, prompt: str, max_new_tokens: int = 400, system_instruction: str = None) -> str:
#         if not self.client:
#             return ""
#         try:
#             config = types.GenerateContentConfig(
#                 temperature=0.1,
#                 max_output_tokens=max_new_tokens,
#                 system_instruction=system_instruction
#             )
#             response = self.client.models.generate_content(
#                 model=self.model_name,
#                 contents=prompt,
#                 config=config
#             )
#             return response.text.strip() if response.text else ""
#         except Exception as e:
#             logger.error(f"Gemini API Processing Execution Fault: {e}")
#             return ""

#     def parse_tests(self, text: str) -> dict:
#         """Forces Gemini to return structured JSON arrays natively."""
#         if not self.client:
#             return {"tests": []}

#         # Define schema layout configuration rules
#         target_json_schema = {
#             "type": "OBJECT",
#             "properties": {
#                 "tests": {
#                     "type": "ARRAY",
#                     "items": {
#                         "type": "OBJECT",
#                         "properties": {
#                             "test_name": {"type": "STRING"},
#                             "value": {"type": "STRING"},
#                             "unit": {"type": "STRING"},
#                             "reference_range": {"type": "STRING"},
#                             "status": {"type": "STRING"}
#                         },
#                         "required": ["test_name", "value", "status"]
#                     }
#                 }
#             },
#             "required": ["tests"]
#         }

#         prompt = f"Extract all laboratory medical findings records into a clean schema layout block:\n\n{text}"
        
#         try:
#             response = self.client.models.generate_content(
#                 model=self.model_name,
#                 contents=prompt,
#                 config=types.GenerateContentConfig(
#                     response_mime_type="application/json",
#                     response_schema=target_json_schema,
#                     temperature=0.1,
#                     system_instruction="You are a precise medical data extraction tool. Extract values exactly as written."
#                 )
#             )
#             return json.loads(response.text)
#         except Exception as e:
#             logger.error(f"JSON structural parser fallback triggered: {e}")
#             return {"tests": []}

# OCRHandling/ensemble_processor.py
# import json
# import logging
# from google import genai
# from google.genai import types

# logger = logging.getLogger(__name__)

# class HFLLMProcessor: 
#     def __init__(self):
#         try:
#             self.client = genai.Client() # Picks up GEMINI_API_KEY automatically
#             self.model_name = "gemini-2.5-flash"
#         except Exception as e:
#             logger.error(f"Failed to initialize Gemini Client: {e}")
#             self.client = None

#     def parse_tests(self, few_shot_prompt: str) -> dict:
#         if not self.client:
#             return {"tests": []}

#         # Strict response constraint matching your target model template
#         lab_schema = {
#             "type": "OBJECT",
#             "properties": {
#                 "tests": {
#                     "type": "ARRAY",
#                     "items": {
#                         "type": "OBJECT",
#                         "properties": {
#                             "test_name": {"type": "STRING"},
#                             "value": {"type": "STRING"},
#                             "unit": {"type": "STRING"},
#                             "reference_range": {"type": "STRING"},
#                             "status": {"type": "STRING"}
#                         },
#                         "required": ["test_name", "value", "status"]
#                     }
#                 }
#             },
#             "required": ["tests"]
#         }

#         try:
#             response = self.client.models.generate_content(
#                 model=self.model_name,
#                 contents=few_shot_prompt,
#                 config=types.GenerateContentConfig(
#                     response_mime_type="application/json",
#                     response_schema=lab_schema,
#                     temperature=0.0  # Eliminate variance entirely
#                 )
#             )
#             return json.loads(response.text)
#         except Exception as e:
#             logger.error(f"Gemini structural extraction breakdown: {e}")
#             return {"tests": []}



import json
import logging
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

# =========================================================
# PYDANTIC STRUCTURED OUTPUT SCHEMA
# =========================================================
class TestItem(BaseModel):
    test_name: str = Field(
        description="The exact name of the diagnostic test or biometric marker (e.g., Hemoglobin, RBC Count, Cholesterol)."
    )
    value: str = Field(
        description="The numeric or qualitative test result value. Strip extra text; keep only the measurement value."
    )
    unit: Optional[str] = Field(
        default="N/A", 
        description="The units of measurement (e.g., g/dL, million/cmm, %). Default to 'N/A' if missing."
    )
    reference_range: Optional[str] = Field(
        default="Normal", 
        description="The normal reference boundaries/intervals (e.g., 13.0 - 16.5, <200)."
    )
    status: str = Field(
        description="The clinical alert indicator classification based on reference bounds. Must be strictly 'Normal', 'High', 'Low', or 'Borderline'."
    )

class LabReportSchema(BaseModel):
    tests: List[TestItem] = Field(
        description="List of all structured clinical test results parsed from the OCR dump."
    )


# =========================================================
# GEMINI GENERATION WORKER CLIENT
# =========================================================
class HFLLMProcessor: 
    def __init__(self):
        try:
            self.client = genai.Client() # Automatically reads GEMINI_API_KEY from environment variables
            self.model_name = "gemini-2.5-flash"
        except Exception as e:
            logger.error(f"Failed to initialize Gemini Client: {e}")
            self.client = None

    def parse_tests(self, few_shot_prompt: str) -> dict:
        if not self.client:
            logger.error("Gemini client is uninitialized. Skipping API execution.")
            return {"tests": []}

        try:
            # Execute Gemini using the native Pydantic schema model
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=few_shot_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=LabReportSchema, # <-- Passes the Pydantic class directly
                    temperature=0.1,                 # Low temperature to preserve structural accuracy
                )
            )

            # Safeguard parsing of the return string block
            raw_text = response.text.strip() if response.text else ""
            if not raw_text:
                logger.warning("Gemini returned empty text content.")
                return {"tests": []}

            parsed_data = json.loads(raw_text)
            return parsed_data

        except Exception as e:
            logger.error(f"❌ Gemini structural extraction breakdown: {e}")
            return {"tests": []}