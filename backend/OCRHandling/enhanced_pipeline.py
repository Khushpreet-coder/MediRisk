# """
# Enhanced OCR + Ensemble LLM Pipeline

# Integrates multi-engine OCR with ensemble LLM validation
# for production-ready medical report processing.
# """

# import logging
# from pathlib import Path
# from typing import Dict, Optional, Tuple
# from PIL import Image
# import json

# from OCRHandling.ocr_service import extract_text as extract_text_single
# from OCRHandling.ensemble_processor import OCRHFEnsemblePipeline, MultiEngineOCR
# from OCRHandling.text_cleaner import clean_text
# from OCRHandling.llm_parser import structure_report
# from OCRHandling.validator import validate_data
# from RAG.rag_service import generate_summary as build_rag_context
# from RAG.llm_summary import generate_medical_summary

# logger = logging.getLogger(__name__)


# # =====================================
# # CONFIDENCE-BASED PROCESSING
# # =====================================


# class AdaptiveOCRPipeline:
#     """
#     Adaptive pipeline that uses confidence scores to decide
#     processing strategy (standard vs ensemble).
#     """

#     LOW_CONFIDENCE_THRESHOLD = 0.65
#     ENSEMBLE_THRESHOLD = 0.70
#     HIGH_CONFIDENCE_THRESHOLD = 0.85

#     def __init__(self):
#         """Initialize pipeline components."""
#         self.ensemble = OCRHFEnsemblePipeline()
#         self.multi_ocr = MultiEngineOCR()

#     def process_report(self, file_path: str) -> Dict:
#         """
#         Process medical report with adaptive confidence-based strategy.

#         Args:
#             file_path: Path to medical report (PDF or image)

#         Returns:
#             Processed report with confidence metrics
#         """
#         logger.info(f"Processing report: {file_path}")

#         # Step 1: Initial OCR extraction
#         raw_text = extract_text_single(file_path)
        
#         if not raw_text:
#             logger.error("Initial OCR extraction failed")
#             return self._failed_result("OCR extraction failed")

#         # Step 2: Clean text
#         cleaned_text = clean_text(raw_text)
#         logger.info(f"Cleaned text length: {len(cleaned_text)} chars")

#         # Step 3: Adaptive processing based on confidence
#         result = self._adaptive_process(cleaned_text)

#         return result

#     def _adaptive_process(self, text: str) -> Dict:
#         """
#         Adaptively choose processing strategy based on confidence.

#         Strategy:
#         - High confidence (>85%): Standard LLM parsing
#         - Medium confidence (70-85%): Ensemble LLM with voting
#         - Low confidence (<70%): Ensemble LLM + human review flag
#         """
#         logger.info("Starting adaptive processing...")

#         # Try standard LLM first to estimate confidence
#         initial_result = structure_report(text)

#         if not initial_result.get("tests"):
#             logger.warning("Initial LLM parsing returned no tests, using ensemble")
#             return self._ensemble_process(text)

#         # Estimate confidence from LLM response
#         avg_confidence = self._estimate_confidence(initial_result)
#         logger.info(f"Estimated initial confidence: {avg_confidence:.2%}")

#         if avg_confidence >= self.HIGH_CONFIDENCE_THRESHOLD:
#             logger.info("High confidence - using standard processing")
#             return {
#                 "tests": initial_result.get("tests", []),
#                 "metrics": {
#                     "confidence": avg_confidence,
#                     "method": "standard_llm",
#                     "strategy": "high_confidence"
#                 }
#             }

#         elif avg_confidence >= self.ENSEMBLE_THRESHOLD:
#             logger.info("Medium confidence - using ensemble validation")
#             ensemble_result = self._ensemble_validate(initial_result, text)
#             return ensemble_result

#         else:
#             logger.warning("Low confidence - using full ensemble processing with review flag")
#             ensemble_result = self._ensemble_process(text)
#             ensemble_result["requires_review"] = True
#             return ensemble_result

#     def _ensemble_process(self, text: str) -> Dict:
#         """Full ensemble processing from cleaned text."""
#         # For text-only input, we need to reconstruct an image or use LLM ensemble directly
#         # Get multiple LLM parses
#         parsed = self.ensemble.llm.parse_tests(text)
#         ensemble_result = parsed.get("tests", [])

#         if not ensemble_result:
#             return self._failed_result("Ensemble processing failed")

#         return {
#             "tests": ensemble_result,
#             "metrics": {
#                 "method": "ensemble_llm",
#                 "strategy": "full_ensemble"
#             }
#         }

#     def _ensemble_validate(self, initial_result: Dict, text: str) -> Dict:
#         """Validate initial result with ensemble LLM voting."""
#         parsed = self.ensemble.llm.parse_tests(text)
#         ensemble_result = parsed.get("tests", [])

#         if not ensemble_result:
#             return {
#                 "tests": initial_result.get("tests", []),
#                 "metrics": {
#                     "method": "standard_llm_fallback",
#                     "strategy": "fallback_to_initial"
#                 }
#             }

#         # Reconcile with initial result
#         reconciled = self._reconcile_results(initial_result, ensemble_result)

#         return {
#             "tests": reconciled,
#             "metrics": {
#                 "method": "ensemble_validated",
#                 "strategy": "confidence_ensemble",
#                 "initial_count": len(initial_result.get("tests", [])),
#                 "ensemble_count": len(ensemble_result)
#             }
#         }

#     def _reconcile_results(self, initial: Dict, ensemble: Dict) -> list:
#         """Reconcile initial and ensemble results."""
#         # For now, prefer ensemble results as they have voting
#         return ensemble

#     def _estimate_confidence(self, result: Dict) -> float:
#         """
#         Estimate confidence from LLM result.

#         Heuristics:
#         - All tests have status → higher confidence
#         - All fields populated → higher confidence
#         - Mixed/missing data → lower confidence
#         """
#         tests = result.get("tests", [])

#         if not tests:
#             return 0.0

#         confidence_scores = []

#         for test in tests:
#             test_conf = 0.0

#             # Field completeness
#             if test.get("test_name"):
#                 test_conf += 0.25
#             if test.get("value"):
#                 test_conf += 0.25
#             if test.get("status"):
#                 test_conf += 0.25
#             if test.get("reference_range"):
#                 test_conf += 0.25

#             confidence_scores.append(test_conf)

#         avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0

#         return avg_confidence

#     def _failed_result(self, reason: str) -> Dict:
#         """Return failed processing result."""
#         logger.error(f"Processing failed: {reason}")
#         return {
#             "tests": [],
#             "metrics": {
#                 "confidence": 0.0,
#                 "method": "failed",
#                 "reason": reason
#             },
#             "requires_review": True
#         }


# # =====================================
# # COMPARATIVE ANALYSIS
# # =====================================


# class OCRComparison:
#     """Compare different OCR and LLM approaches."""

#     @staticmethod
#     def compare_ocr_engines(image_path: str) -> Dict:
#         """
#         Compare Tesseract vs EasyOCR on same image.

#         Args:
#             image_path: Path to image file

#         Returns:
#             Comparison results with metrics
#         """
#         image = Image.open(image_path)
#         multi_ocr = MultiEngineOCR()

#         tesseract_text, tesseract_conf = multi_ocr.ocr_tesseract(image)
#         easyocr_text, easyocr_conf = multi_ocr.ocr_easyocr(image)

#         return {
#             "comparison": {
#                 "tesseract": {
#                     "confidence": tesseract_conf,
#                     "text_length": len(tesseract_text),
#                     "preview": tesseract_text[:200]
#                 },
#                 "easyocr": {
#                     "confidence": easyocr_conf,
#                     "text_length": len(easyocr_text),
#                     "preview": easyocr_text[:200]
#                 },
#                 "winner": "easyocr" if easyocr_conf > tesseract_conf else "tesseract",
#                 "confidence_diff": abs(easyocr_conf - tesseract_conf)
#             }
#         }

# @staticmethod
# def compare_llm_models(text: str) -> Dict:
#     """
#     Compare results from different LLM models.
#     """

#     ensemble = OCRHFEnsemblePipeline()

#     results = {}

#     models = ["flan-t5-base", "flan-t5-small"]

#     for model in models:
#         try:
#             result = ensemble.llm.parse_tests(text)

#             results[model] = {
#                 "test_count": len(result.get("tests", [])),
#                 "tests": result.get("tests", [])
#             }

#         except Exception as e:
#             results[model] = {
#                 "error": str(e)
#             }

#     return {
#         "model_comparison": results
#     }


# # =====================================
# # MAIN PROCESSING FUNCTIONS
# # =====================================


# def process_report_enhanced(
#     file_path: str,
#     use_ensemble: bool = False,
#     output_path: Optional[str] = None
# ) -> Dict:

#     pipeline = AdaptiveOCRPipeline()

#     if use_ensemble:
#         logger.info("Using forced ensemble processing")
#         raw_text = extract_text_single(file_path)
#         cleaned_text = clean_text(raw_text)
#         result = pipeline._ensemble_process(cleaned_text)
#     else:
#         result = pipeline.process_report(file_path)

#     # -----------------------------
#     # VALIDATION
#     # -----------------------------
#     if result["tests"] and not validate_data({"tests": result["tests"]}):
#         result["requires_review"] = True

#     # -----------------------------
#     # 🔥 STEP 1: BUILD RAG CONTEXT
#     # -----------------------------
#     rag_output = build_rag_context({
#         "tests": result.get("tests", [])
#     })

#     rag_context = rag_output.get("rag_context", [])

#     # -----------------------------
#     # 🔥 STEP 2: ATTACH TO RESULT
#     # -----------------------------
#     # -----------------------------
#     # 🔥 STEP 2: ATTACH TO RESULT
#     # -----------------------------
#     result["rag_context"] = rag_context

#     # Optional: also keep cleaned text
#     result["cleaned_text"] = clean_text(extract_text_single(file_path))

#     # -----------------------------
#     # 🔥 STEP 3: GENERATE SUMMARY   ← ADD HERE
#     # -----------------------------
#     result["summary"] = generate_medical_summary(result)

#     # -----------------------------
#     # SAVE
#     # -----------------------------
#     if output_path:
#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=2, ensure_ascii=False)

#     return result


# def compare_approaches(image_path: str) -> Dict:
#     """
#     Compare different OCR and LLM approaches on same image.

#     Useful for benchmarking and optimization.
#     """
#     return {
#         "ocr_comparison": OCRComparison.compare_ocr_engines(image_path),
#         # LLM comparison would need extracted text first
#     }


# """
# Streamlined Production OCR Pipeline
# Handles clean linear parsing utilizing the native power of Gemini.
# """

# import logging
# import json
# from pathlib import Path
# from typing import Dict, Optional

# from OCRHandling.ocr_service import extract_text as extract_text_single
# from OCRHandling.ensemble_processor import HFLLMProcessor
# from OCRHandling.text_cleaner import clean_text
# from OCRHandling.validator import validate_data
# from RAG.rag_service import generate_summary as build_rag_context
# from RAG.llm_summary import generate_medical_summary

# logger = logging.getLogger(__name__)

# class AdaptiveOCRPipeline:
#     """
#     Simplified pipeline executing fast, structured cloud analysis.
#     """
#     def __init__(self):
#         self.processor = HFLLMProcessor()

#     def process_report(self, file_path: str) -> Dict:
#         logger.info(f"Processing report: {file_path}")

#         # 1. OCR Step
#         raw_text = extract_text_single(file_path)
#         if not raw_text:
#             return {"tests": [], "error": "OCR extraction failed"}

#         # 2. Cleanup text
#         cleaned_text = clean_text(raw_text)

#         # 3. Structural Extraction via Gemini
#         parsed_result = self.processor.parse_tests(cleaned_text)
#         tests = parsed_result.get("tests", [])

#         return {
#             "tests": tests,
#             "metrics": {
#                 "method": "gemini_native_flash",
#                 "strategy": "direct_extraction"
#             }
#         }


# # enhanced_pipeline.py

# def process_report_enhanced(file_path: str, use_ensemble: bool = False, output_path: Optional[str] = None) -> Dict:
#     pipeline = AdaptiveOCRPipeline()
    
#     # 1. Check Raw OCR Text Output
#     result = pipeline.process_report(file_path)
    
#     print("\n=======================================================")
#     print("🔍 STEP 1: RAW CLEANED OCR TEXT")
#     print("=======================================================")
#     print(result.get("cleaned_text", "No text extracted."))
    
#     # 2. Check Structured JSON Output
#     print("\n=======================================================")
#     print("📊 STEP 2: STRUCTURED REPORT JSON")
#     print("=======================================================")
#     print(json.dumps({"tests": result.get("tests", [])}, indent=2))

#     # Validate output elements
#     if result["tests"] and not validate_data({"tests": result["tests"]}):
#         result["requires_review"] = True

#     # 3. Check RAG Context Processing
#     rag_output = build_rag_context({"tests": result.get("tests", [])})
#     result["rag_context"] = rag_output.get("rag_context", [])
    
#     print("\n=======================================================")
#     print("📚 STEP 3: RETRIEVED RAG MEDICAL CONTEXT")
#     print("=======================================================")
#     print(json.dumps(result["rag_context"], indent=2))

#     # 4. Check Final Patient-Friendly Summary
#     result["summary"] = generate_medical_summary(result)
    
#     print("\n=======================================================")
#     print("📝 STEP 4: FINAL CLINICAL EXECUTIVE SUMMARY")
#     print("=======================================================")
#     print(result["summary"])
#     print("=======================================================\n")

#     if output_path:
#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=2, ensure_ascii=False)

#     return result

# """
# Streamlined Production OCR Pipeline
# Handles clean linear parsing utilizing the native power of Gemini and Groq.
# """

# import logging
# import json
# from pathlib import Path
# from typing import Dict, Optional

# from OCRHandling.ocr_service import extract_text as extract_text_single
# from OCRHandling.text_cleaner import clean_text
# from OCRHandling.validator import validate_data
# from OCRHandling.llm_parser import structure_report        # <-- Import your few-shot routing engine
# from RAG.rag_service import generate_summary  
# from RAG.llm_summary import generate_medical_summary
# # from RAG.rag_service import build_rag_context


# logger = logging.getLogger(__name__)

# class AdaptiveOCRPipeline:
#     """
#     Simplified pipeline executing fast, structured cloud analysis.
#     """
#     def __init__(self):
#         pass # Processor handling moved cleanly to the llm_parser module

#     def process_report(self, file_path: str) -> Dict:
#         logger.info(f"Processing report: {file_path}")

#         # 1. OCR Step
#         raw_text = extract_text_single(file_path)
#         if not raw_text:
#             logger.error("OCR raw text extraction returned empty.")
#             return {"tests": [], "cleaned_text": "", "error": "OCR extraction failed"}

#         # 2. Cleanup text
#         cleaned_text = clean_text(raw_text)

#         # 3. Structural Extraction via your custom Few-Shot LLM Parser module
#         parsed_result = structure_report(cleaned_text)
#         tests = parsed_result.get("tests", [])

#         # Return EVERYTHING needed downstream
#         return {
#             "cleaned_text": cleaned_text, # <-- CRITICAL FIX: Sent to routes/terminal prints
#             "tests": tests,
#             "metrics": {
#                 "method": "gemini_native_flash",
#                 "strategy": "few_shot_direct_extraction"
#             },
#             "requires_review": False
#         }


# # =========================================================
# # CORE ANCHOR ENHANCED RUNNER
# # =========================================================

# def process_report_enhanced(file_path: str, use_ensemble: bool = False, output_path: Optional[str] = None) -> Dict:
#     pipeline = AdaptiveOCRPipeline()
    
#     # Execute the core extraction and parsing step
#     result = pipeline.process_report(file_path)
    
#     # 1. Check Raw OCR Text Output
#     print("\n=======================================================")
#     print("🔍 STEP 1: RAW CLEANED OCR TEXT")
#     print("=======================================================")
#     print(result.get("cleaned_text", "No text extracted."))
    
#     # 2. Check Structured JSON Output
#     print("\n=======================================================")
#     print("📊 STEP 2: STRUCTURED REPORT JSON")
#     print("=======================================================")
#     print(json.dumps({"tests": result.get("tests", [])}, indent=2))

#     # Validate output elements
#     if result["tests"] and not validate_data({"tests": result["tests"]}):
#         result["requires_review"] = True

#     # 3. Check RAG Context Processing
#     rag_output =generate_summary({"tests": result.get("tests", [])})
#     result["rag_context"] = rag_output.get("rag_context", [])
    
#     print("\n=======================================================")
#     print("📚 STEP 3: RETRIEVED RAG MEDICAL CONTEXT")
#     print("=======================================================")
#     print(json.dumps(result["rag_context"], indent=2))

#     # 4. Check Final Patient-Friendly Summary (Now routing to Groq internally!)
#     result["summary"] = generate_medical_summary(result)
    
#     print("\n=======================================================")
#     print("📝 STEP 4: FINAL CLINICAL EXECUTIVE SUMMARY")
#     print("=======================================================")
#     print(result["summary"])
#     print("=======================================================\n")

#     if output_path:
#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=2, ensure_ascii=False)

#     return result


# """
# Streamlined Production OCR Pipeline
# Handles clean linear parsing utilizing the native power of Gemini and Groq.
# """

# import logging
# import json
# from pathlib import Path
# from typing import Dict, Optional

# from OCRHandling.ocr_service import extract_text as extract_text_single
# from OCRHandling.text_cleaner import clean_text
# from OCRHandling.validator import validate_data
# from OCRHandling.llm_parser import structure_report        # <-- Import your few-shot routing engine
# from RAG.rag_service import generate_summary  
# from RAG.llm_summary import generate_medical_summary
# # from RAG.rag_service import build_rag_context


# logger = logging.getLogger(__name__)

# class AdaptiveOCRPipeline:
#     """
#     Simplified pipeline executing fast, structured cloud analysis.
#     """
#     def __init__(self):
#         pass # Processor handling moved cleanly to the llm_parser module

#     def process_report(self, file_path: str) -> Dict:
#         logger.info(f"Processing report: {file_path}")

#         # 1. OCR Step
#         raw_text = extract_text_single(file_path)
#         if not raw_text:
#             logger.error("OCR raw text extraction returned empty.")
#             return {"tests": [], "cleaned_text": "", "error": "OCR extraction failed"}

#         # 2. Cleanup text
#         cleaned_text = clean_text(raw_text)

#         # 3. Structural Extraction via your custom Few-Shot LLM Parser module
#         parsed_result = structure_report(cleaned_text)
#         tests = parsed_result.get("tests", [])

#         # Return EVERYTHING needed downstream
#         return {
#             "cleaned_text": cleaned_text, # <-- CRITICAL FIX: Sent to routes/terminal prints
#             "tests": tests,
#             "metrics": {
#                 "method": "gemini_native_flash",
#                 "strategy": "few_shot_direct_extraction"
#             },
#             "requires_review": False
#         }


# # =========================================================
# # CORE ANCHOR ENHANCED RUNNER
# # =========================================================

# def process_report_enhanced(file_path: str, use_ensemble: bool = False, output_path: Optional[str] = None) -> Dict:
#     pipeline = AdaptiveOCRPipeline()
    
#     # Execute the core extraction and parsing step
#     result = pipeline.process_report(file_path)
    
#     # 1. Check Raw OCR Text Output
#     print("\n=======================================================")
#     print("🔍 STEP 1: RAW CLEANED OCR TEXT")
#     print("=======================================================")
#     print(result.get("cleaned_text", "No text extracted."))
    
#     # 2. Check Structured JSON Output
#     print("\n=======================================================")
#     print("📊 STEP 2: STRUCTURED REPORT JSON")
#     print("=======================================================")
#     print(json.dumps({"tests": result.get("tests", [])}, indent=2))

#     # Validate output elements
#     if result["tests"] and not validate_data({"tests": result["tests"]}):
#         result["requires_review"] = True

#     # 3. Check RAG Context Processing
#     rag_output =generate_summary({"tests": result.get("tests", [])})
#     result["rag_context"] = rag_output.get("rag_context", [])
    
#     print("\n=======================================================")
#     print("📚 STEP 3: RETRIEVED RAG MEDICAL CONTEXT")
#     print("=======================================================")
#     print(json.dumps(result["rag_context"], indent=2))

#     # 4. Check Final Patient-Friendly Summary (Now routing to Groq internally!)
#     result["summary"] = generate_medical_summary(result)
    
#     print("\n=======================================================")
#     print("📝 STEP 4: FINAL CLINICAL EXECUTIVE SUMMARY")
#     print("=======================================================")
#     print(result["summary"])
#     print("=======================================================\n")

#     if output_path:
#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=2, ensure_ascii=False)

#     return result

"""
Streamlined Production OCR Pipeline
Handles clean linear parsing utilizing the native power of Gemini and Groq.
"""

import logging
import json
from pathlib import Path
from typing import Dict, Optional

from OCRHandling.ocr_service import extract_text as extract_text_single
from OCRHandling.text_cleaner import clean_text
from OCRHandling.validator import validate_data
from OCRHandling.llm_parser import structure_report        # <-- Import your few-shot routing engine

# ✅ ALIAS THE IMPORT: Prevents Python name collisions with local pipeline logic
from RAG.rag_service import generate_summary as run_knowledge_base_retrieval  
from RAG.llm_summary import generate_medical_summary


logger = logging.getLogger(__name__)

class AdaptiveOCRPipeline:
    """
    Simplified pipeline executing fast, structured cloud analysis.
    """
    def __init__(self):
        pass # Processor handling moved cleanly to the llm_parser module

    def process_report(self, file_path: str) -> Dict:
        logger.info(f"Processing report: {file_path}")

        # 1. OCR Step
        raw_text = extract_text_single(file_path)
        if not raw_text:
            logger.error("OCR raw text extraction returned empty.")
            return {"tests": [], "cleaned_text": "", "error": "OCR extraction failed"}

        # 2. Cleanup text
        cleaned_text = clean_text(raw_text)

        # 3. Structural Extraction via your custom Few-Shot LLM Parser module
        parsed_result = structure_report(cleaned_text)
        tests = parsed_result.get("tests", [])

        # Return EVERYTHING needed downstream
        return {
            "cleaned_text": cleaned_text, # <-- CRITICAL FIX: Sent to routes/terminal prints
            "tests": tests,
            "metrics": {
                "method": "gemini_native_flash",
                "strategy": "few_shot_direct_extraction"
            },
            "requires_review": False
        }


# =========================================================
# CORE ANCHOR ENHANCED RUNNER
# =========================================================

# def process_report_enhanced(file_path: str, use_ensemble: bool = False, output_path: Optional[str] = None) -> Dict:
#     pipeline = AdaptiveOCRPipeline()
    
#     # Execute the core extraction and parsing step
#     result = pipeline.process_report(file_path)
    
#     # 1. Check Raw OCR Text Output
#     print("\n=======================================================")
#     print("🔍 STEP 1: RAW CLEANED OCR TEXT")
#     print("=======================================================")
#     print(result.get("cleaned_text", "No text extracted."))
    
#     # 2. Check Structured JSON Output
#     print("\n=======================================================")
#     print("📊 STEP 2: STRUCTURED REPORT JSON")
#     print("=======================================================")
#     print(json.dumps({"tests": result.get("tests", [])}, indent=2))

#     # Validate output elements
#     if result["tests"] and not validate_data({"tests": result["tests"]}):
#         result["requires_review"] = True

#     # 3. Check RAG Context Processing
#     # ✅ CALL THE ALIASED FUNCTION: Avoids namespaces collisions cleanly
#     rag_output = run_knowledge_base_retrieval({"tests": result.get("tests", [])})
#     result["rag_context"] = rag_output.get("rag_context", [])
    
#     print("\n=======================================================")
#     print("📚 STEP 3: RETRIEVED RAG MEDICAL CONTEXT")
#     print("=======================================================")
#     print(json.dumps(result["rag_context"], indent=2))

#     # 4. Check Final Patient-Friendly Summary (Now routing to Groq internally!)
#     result["summary"] = generate_medical_summary(result)
    
#     print("\n=======================================================")
#     print("📝 STEP 4: FINAL CLINICAL EXECUTIVE SUMMARY")
#     print("=======================================================")
#     print(result["summary"])
#     print("=======================================================\n")

#     if output_path:
#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(result, f, indent=2, ensure_ascii=False)

#     return result

def process_report_enhanced(file_path: str, use_ensemble: bool = False, output_path: Optional[str] = None) -> Dict:
    pipeline = AdaptiveOCRPipeline()
    
    # Execute the core extraction and parsing step
    result = pipeline.process_report(file_path)
    
    # --- CRITICAL VERIFICATION ---
    # We explicitly verify that 'tests' exists and report its count before further processing
    tests_list = result.get("tests", [])
    print(f"DEBUG: Pipeline tests count: {len(tests_list)}")
    
    # 1. Check Raw OCR Text Output
    print("\n=======================================================")
    print("🔍 STEP 1: RAW CLEANED OCR TEXT")
    print("=======================================================")
    print(result.get("cleaned_text", "No text extracted."))
    
    # 2. Check Structured JSON Output
    print("\n=======================================================")
    print("📊 STEP 2: STRUCTURED REPORT JSON")
    print("=======================================================")
    print(json.dumps({"tests": tests_list}, indent=2))

    # Validate output elements
    if tests_list and not validate_data({"tests": tests_list}):
        result["requires_review"] = True
    else:
        result["requires_review"] = False

    # 3. Check RAG Context Processing
    rag_output = run_knowledge_base_retrieval({"tests": tests_list})
    result["rag_context"] = rag_output.get("rag_context", [])
    
    print("\n=======================================================")
    print("📚 STEP 3: RETRIEVED RAG MEDICAL CONTEXT")
    print("=======================================================")
    print(json.dumps(result["rag_context"], indent=2))

    # 4. Check Final Patient-Friendly Summary
    # Ensure the full dictionary contains 'tests' and 'rag_context' so Groq has full data
    result["tests"] = tests_list
    result["summary"] = generate_medical_summary(result)
    
    print("\n=======================================================")
    print("📝 STEP 4: FINAL CLINICAL EXECUTIVE SUMMARY")
    print("=======================================================")
    print(result["summary"])
    print("=======================================================\n")

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    return result