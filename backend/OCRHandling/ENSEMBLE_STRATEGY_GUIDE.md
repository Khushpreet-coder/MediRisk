# OCR + Ensemble LLM Strategy Guide

## Overview

This guide explains how to use **multi-engine OCR + ensemble LLMs** for high-accuracy medical text extraction. The system combines the best of both worlds:

- **Multi-Engine OCR**: Tesseract + EasyOCR
- **Ensemble LLMs**: Multiple Groq models with voting
- **Confidence Scoring**: Track reliability of results
- **Adaptive Processing**: Smart selection of extraction strategy

---

## Architecture

### 1. Multi-Engine OCR

```
Input Image
    ↓
├─→ Tesseract OCR → Text + Confidence Score
│
└─→ EasyOCR → Text + Confidence Score
    ↓
Select Best Result (highest confidence)
    ↓
Output: Best OCR Text
```

**Why Multiple Engines?**
- Tesseract: Fast, lightweight, good for high-contrast documents
- EasyOCR: Modern deep learning, better for handwriting and unusual formats
- Ensemble: Always uses the most confident result

**Usage:**
```python
from OCRHandling.ensemble_processor import MultiEngineOCR

ocr = MultiEngineOCR()
image = Image.open("report.png")

# Get best result from both engines
text, confidence = ocr.extract_ensemble(image)
print(f"Confidence: {confidence:.1%}")
```

### 2. Ensemble LLM Validation

```
Extracted Text
    ↓
├─→ Model 1 (llama-3.3-70b) → Test results + parsing
│
├─→ Model 2 (llama-3.1-70b) → Test results + parsing
│
└─→ Model N (other models) → Test results + parsing
    ↓
Vote on Results (consensus)
    ↓
Output: Reconciled tests with agreement scores
```

**Voting Mechanism:**
```
For each test:
  - Count votes for: test_name, value, unit, status
  - Pick most common (highest agreement)
  - Calculate confidence = votes_for_best / total_votes
```

**Usage:**
```python
from OCRHandling.ensemble_processor import EnsembleLLMValidator

validator = EnsembleLLMValidator()

# Get consensus from multiple models
tests = validator.validate_with_multiple_models(cleaned_text)

# Tests now include:
# - test_name
# - value
# - unit
# - reference_range
# - status
# - confidence (agreement score)
# - agreement (ratio of models agreeing)
```

### 3. Adaptive Processing Strategy

```
Initial Confidence Estimation
    ↓
If confidence >= 85%
    └─→ Use Standard LLM (fast)
    
If confidence 70-85%
    └─→ Use Ensemble LLM (medium speed, better accuracy)
    
If confidence < 70%
    └─→ Use Full Ensemble + Flag for human review
```

**Usage:**
```python
from OCRHandling.enhanced_pipeline import AdaptiveOCRPipeline

pipeline = AdaptiveOCRPipeline()
result = pipeline.process_report("report.pdf")

# Result includes:
# - tests: extracted tests
# - metrics: confidence, method used, strategy
# - requires_review: flag if low confidence
```

---

## Implementation Guide

### Step 1: Install Dependencies

```bash
pip install easyocr opencv-python pillow groq pytesseract fitz
```

### Step 2: Use Enhanced Pipeline

```python
from OCRHandling.enhanced_pipeline import process_report_enhanced

# Adaptive processing (recommended)
result = process_report_enhanced(
    file_path="report.pdf",
    use_ensemble=False,  # Auto-decide based on confidence
    output_path="result.json"
)

print(f"Tests extracted: {len(result['tests'])}")
print(f"Average confidence: {result['metrics']['confidence']:.1%}")
print(f"Method used: {result['metrics']['method']}")
```

### Step 3: Force Ensemble for Critical Reports

```python
# For high-stakes medical reports, always use ensemble
result = process_report_enhanced(
    file_path="critical_report.pdf",
    use_ensemble=True,  # Force ensemble processing
    output_path="critical_result.json"
)

if result.get("requires_review"):
    print("⚠️ Human review recommended")
```

### Step 4: Compare Approaches

```python
from OCRHandling.enhanced_pipeline import OCRComparison

# See which OCR engine performs better
comparison = OCRComparison.compare_ocr_engines("test_image.png")

print(f"Tesseract confidence: {comparison['comparison']['tesseract']['confidence']:.1%}")
print(f"EasyOCR confidence: {comparison['comparison']['easyocr']['confidence']:.1%}")
print(f"Winner: {comparison['comparison']['winner']}")
```

---

## Confidence Metrics Explained

### OCR Confidence
- **Tesseract**: Average word-level confidence (0-100)
- **EasyOCR**: Average character-level confidence (0-1)
- **Normalized**: Both to 0-1 scale

### LLM Agreement
- **Individual Test Agreement**: % of models that agree on this value
- **Average Confidence**: Mean agreement across all tests
- **Flags for Review**: If < 70% agreement

### Result Metrics

```json
{
  "metrics": {
    "confidence": 0.85,           // Overall confidence (0-1)
    "method": "ensemble_validated", // Processing method used
    "strategy": "medium_confidence", // Strategy chosen
    "initial_count": 12,          // Tests found by first pass
    "ensemble_count": 12          // Tests validated by ensemble
  }
}
```

---

## When to Use Each Strategy

### Standard LLM (Fast, Baseline)
- ✅ Development/testing
- ✅ High-quality scans with good OCR
- ✅ Real-time processing requirements
- ❌ Critical medical decisions
- ❌ Poor quality scans

**Configuration:**
```python
result = structure_report(cleaned_text)  # Direct call
```

### Ensemble LLM (Recommended)
- ✅ Production deployment
- ✅ Medium-confidence reports
- ✅ Batch processing with time available
- ✅ Medical accuracy important
- ❌ Real-time constraints

**Configuration:**
```python
result = process_report_enhanced(file_path, use_ensemble=False)
# Auto-decides to use ensemble if confidence < 85%
```

### Full Ensemble + Review (Maximum Accuracy)
- ✅ Critical medical decisions
- ✅ Low-quality documents
- ✅ Unusual formats
- ✅ Patient safety critical
- ❌ Need instant results

**Configuration:**
```python
result = process_report_enhanced(file_path, use_ensemble=True)
# Always uses ensemble, flags uncertain results
```

---

## Error Handling

```python
from OCRHandling.enhanced_pipeline import process_report_enhanced

try:
    result = process_report_enhanced("report.pdf")
    
    # Check confidence
    if result['metrics']['confidence'] < 0.70:
        print("⚠️ Low confidence - consider manual review")
    
    # Check if review needed
    if result.get("requires_review"):
        print("⚠️ Manual review recommended")
        # Send to review queue
    
    # Check for failures
    if not result['tests']:
        print("❌ No tests extracted")
        # Handle extraction failure
        
except Exception as e:
    print(f"❌ Processing failed: {e}")
    # Handle gracefully
```

---

## Performance Tuning

### Fast Mode (Best for development)
```python
# Use standard LLM only
from OCRHandling.llm_parser import structure_report

result = structure_report(cleaned_text)
# ~2-3 seconds per report
```

### Balanced Mode (Recommended for production)
```python
# Adaptive processing
result = process_report_enhanced(file_path, use_ensemble=False)
# ~3-5 seconds per report
# Automatically uses ensemble only when needed
```

### Accurate Mode (Best for critical reports)
```python
# Force ensemble
result = process_report_enhanced(file_path, use_ensemble=True)
# ~8-12 seconds per report (multiple LLM calls)
# Highest accuracy, highest cost
```

---

## Cost Optimization

### API Calls Per Strategy

**Standard LLM:**
- 1 OCR extraction
- 1 LLM parse
- **Total**: 1 LLM call

**Ensemble LLM (if triggered):**
- 1 OCR extraction
- 1 initial LLM parse (fast check)
- 2-3 ensemble LLM calls (validation)
- **Total**: 3-4 LLM calls

**Full Ensemble:**
- 1 OCR extraction
- 2-3 LLM calls (multiple models)
- **Total**: 2-3 LLM calls

### Cost per Report

Assuming Groq API pricing:
- **Standard**: ~$0.02-0.05
- **Ensemble**: ~$0.05-0.10
- **Full Ensemble**: ~0.04-0.08

**Pro Tip**: Use adaptive mode to minimize costs while maintaining accuracy.

---

## Testing & Validation

```python
from OCRHandling.enhanced_pipeline import OCRComparison
import json

# Test on sample images
test_images = [
    "high_quality.png",
    "low_quality.png",
    "handwritten.png"
]

results = {}
for image in test_images:
    comparison = OCRComparison.compare_ocr_engines(image)
    results[image] = comparison

# Save comparison
with open("ocr_comparison.json", "w") as f:
    json.dump(results, f, indent=2)
```

---

## Troubleshooting

### Low OCR Confidence
```
Cause: Poor image quality
Fix: 
  - Increase image resolution
  - Improve lighting/contrast
  - Use ensemble pipeline (will trigger automatically)
```

### Low LLM Agreement
```
Cause: Ambiguous text or parsing issues
Fix:
  - Review flagged results manually
  - Improve OCR preprocessing
  - Check if document format is unusual
```

### High Processing Time
```
Cause: Ensemble processing triggered
Fix:
  - Use standard mode if speed critical
  - Or accept longer processing for accuracy
  - Monitor confidence scores to understand triggers
```

---

## Next Steps

1. ✅ Deploy enhanced pipeline
2. ✅ Monitor confidence metrics
3. ✅ Adjust thresholds based on your accuracy requirements
4. ✅ Collect metrics on processing time vs accuracy
5. ✅ Fine-tune for your specific document types

---

## References

- **Tesseract Docs**: https://github.com/UB-Mannheim/tesseract/wiki
- **EasyOCR**: https://github.com/JaidedAI/EasyOCR
- **Groq API**: https://console.groq.com/docs
