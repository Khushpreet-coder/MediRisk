# """
# Configuration for OCR + Ensemble LLM Processing

# This file defines thresholds, models, and strategies for the ensemble processing pipeline.
# """

# # =====================================
# # CONFIDENCE THRESHOLDS
# # =====================================

# # Minimum confidence to consider result valid
# MIN_ACCEPTABLE_CONFIDENCE = 0.65

# # Threshold to use standard processing (no ensemble)
# HIGH_CONFIDENCE_THRESHOLD = 0.85

# # Threshold to use ensemble validation
# ENSEMBLE_THRESHOLD = 0.70

# # Threshold to flag result for human review
# REVIEW_THRESHOLD = 0.60

# # =====================================
# # OCR ENGINES
# # =====================================

# # Enable/disable specific OCR engines
# OCR_ENGINES = {
#     "tesseract": {
#         "enabled": True,
#         "weight": 0.5,  # Importance weight in ensemble
#         "description": "Fast, traditional OCR"
#     },
#     "easyocr": {
#         "enabled": True,
#         "weight": 0.5,
#         "description": "Deep learning-based OCR"
#     }
# }

# # Tesseract configuration
# TESSERACT_CONFIG = {
#     "oem": 3,           # OCR Engine Mode: 3 = LSTM neural network
#     "psm": 3,           # Page Segmentation Mode: 3 = Auto with OSD
#     "timeout": 30,      # Timeout in seconds
#     "upscale_factor": 4 # Image upscaling before OCR
# }

# # =====================================
# # LLM MODELS
# # =====================================

# # Primary LLM models for ensemble
# LLM_MODELS = [
#     {
#         "name": "llama-3.1-70b-versatile",
#         "provider": "groq",
#         "weight": 0.6,
#         "timeout": 30,
#         "description": "Latest Groq model, best accuracy"
#     },
#     {
#         "name": "llama-3.1-8b-instant",
#         "provider": "groq",
#         "weight": 0.4,
#         "timeout": 30,
#         "description": "Alternative model for validation"
#     }
# ]

# # =====================================
# # PROCESSING STRATEGIES
# # =====================================

# STRATEGIES = {
#     "standard": {
#         "description": "Single LLM pass (fastest)",
#         "confidence_range": (0.85, 1.0),
#         "ocr_engines": 1,
#         "llm_calls": 1,
#         "avg_time": "2-3 seconds",
#         "cost_level": "low",
#         "accuracy": "~80%"
#     },
#     "adaptive": {
#         "description": "Smart choice based on confidence",
#         "confidence_range": (0.65, 1.0),
#         "ocr_engines": 2,
#         "llm_calls": "1-3",
#         "avg_time": "3-5 seconds",
#         "cost_level": "medium",
#         "accuracy": "~90%"
#     },
#     "ensemble": {
#         "description": "Multiple LLMs with voting",
#         "confidence_range": (0.0, 0.7),
#         "ocr_engines": 2,
#         "llm_calls": 2-3,
#         "avg_time": "8-12 seconds",
#         "cost_level": "high",
#         "accuracy": "~95%"
#     }
# }

# # =====================================
# # TEXT CLEANING OPTIONS
# # =====================================

# TEXT_CLEANING = {
#     "remove_ocr_noise": True,
#     "normalize_medical_numbers": True,
#     "fix_common_misreadings": True,
#     "preserve_formatting": False,
#     "remove_page_artifacts": True
# }

# # =====================================
# # VALIDATION RULES
# # =====================================

# VALIDATION_RULES = {
#     "require_test_name": True,
#     "require_value": True,
#     "require_status": False,  # Optional, best effort
#     "min_tests": 1,
#     "max_tests": 200,
#     "allow_text_values": True,  # e.g., "Positive", "Negative"
#     "allow_missing_ranges": True
# }

# # =====================================
# # LOGGING & MONITORING
# # =====================================

# LOGGING = {
#     "level": "INFO",
#     "log_ocr_confidence": True,
#     "log_llm_calls": True,
#     "log_processing_time": True,
#     "save_ocr_intermediate": False  # Debug: save OCR outputs
# }

# # =====================================
# # API CONFIGURATION
# # =====================================

# API = {
#     "groq_timeout": 30,
#     "groq_retry_attempts": 3,
#     "groq_retry_delay": 1,  # seconds
#     "rate_limit": 100  # requests per minute
# }

# # =====================================
# # PERFORMANCE TUNING
# # =====================================

# PERFORMANCE = {
#     "batch_size": 10,                    # Process multiple reports
#     "parallel_processing": False,         # Not thread-safe with current setup
#     "cache_ocr_results": False,
#     "cache_llm_results": False,
#     "max_workers": 1                     # Thread pool size if parallel enabled
# }

# # =====================================
# # FEATURE FLAGS
# # =====================================

# FEATURES = {
#     "use_multi_ocr": True,
#     "use_ensemble_llm": True,
#     "use_adaptive_strategy": True,
#     "confidence_scoring": True,
#     "auto_review_flagging": True,
#     "comparison_mode": False  # Debug: compare all approaches
# }

# # =====================================
# # RESPONSE FORMAT
# # =====================================

# RESPONSE_FORMAT = {
#     "include_confidence": True,
#     "include_processing_time": True,
#     "include_method_used": True,
#     "include_raw_ocr_text": False,  # Can be large, disable for production
#     "include_warnings": True,
#     "pretty_print": False
# }

# # =====================================
# # HELPER FUNCTIONS
# # =====================================


# def get_strategy_for_confidence(confidence: float) -> str:
#     """Determine best strategy based on confidence."""
#     if confidence >= HIGH_CONFIDENCE_THRESHOLD:
#         return "standard"
#     elif confidence >= ENSEMBLE_THRESHOLD:
#         return "adaptive"
#     else:
#         return "ensemble"


# def should_flag_for_review(confidence: float) -> bool:
#     """Check if result should be flagged for human review."""
#     return confidence < REVIEW_THRESHOLD


# def get_processing_time_estimate(strategy: str) -> str:
#     """Get estimated processing time for strategy."""
#     return STRATEGIES.get(strategy, {}).get("avg_time", "unknown")


# def get_cost_estimate(strategy: str) -> str:
#     """Get cost level for strategy."""
#     return STRATEGIES.get(strategy, {}).get("cost_level", "unknown")

import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from google.api_core import exceptions
import google.generativeai as genai  # Assuming you are using the official Google SDK

logger = logging.getLogger(__name__)

class HFLLMProcessor:
    def __init__(self):
        """
        Initializes the Gemini processor. 
        Ensure you have configured your API key elsewhere or via env variables.
        """
        # Replace with your model initialization logic
        self.model = genai.GenerativeModel('gemini-1.5-flash') 

    def format_output(self, raw_text: str) -> dict:
        """
        Helper to clean up LLM output, remove markdown blocks, and parse to JSON.
        """
        import json
        import re
        
        # Remove potential markdown code blocks
        clean_text = re.sub(r'```json|```', '', raw_text).strip()
        try:
            return json.loads(clean_text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON: {e}")
            return {"tests": []}

    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=2, max=10),
        # Only retry on transient server errors (503, 500)
        retry=lambda e: isinstance(e, (exceptions.ServiceUnavailable, exceptions.InternalServerError)),
        before_sleep=lambda retry_state: logger.info(f"Gemini API busy, retrying... Attempt {retry_state.attempt_number}")
    )
    def parse_tests(self, prompt: str) -> dict:
        """
        Sends the prompt to Gemini with built-in retry logic.
        """
        try:
            logger.info("Sending prompt to Gemini engine...")
            response = self.model.generate_content(prompt)
            
            if not response.text:
                raise ValueError("Received empty response from Gemini.")
                
            return self.format_output(response.text)
            
        except Exception as e:
            # Check if this is a transient error; if so, raise it to trigger 'tenacity' retry
            if isinstance(e, (exceptions.ServiceUnavailable, exceptions.InternalServerError)):
                logger.warning(f"Transient error detected: {e}")
                raise e 
            else:
                # Permanent error (e.g., Auth failure, Invalid Prompt), don't retry
                logger.error(f"Permanent API error: {e}")
                return {"tests": [], "error": str(e)}
