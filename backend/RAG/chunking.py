# import re
# from typing import List, Dict


# # =====================================
# # Granular Chunking for RAG
# # =====================================

# def extract_test_name_from_content(content: str) -> str:
#     """Extract test name from content header."""
#     lines = content.split('\n')
#     for line in lines:
#         if line.startswith('Test:'):
#             test_name = line.replace('Test:', '').strip()
#             # Get just the main test name (before parentheses)
#             return test_name.split('(')[0].strip()
#     return ""


# def chunk_knowledge_base(text: str, filename: str) -> List[Dict]:
#     """
#     Create granular, metadata-rich chunks from knowledge base files.
    
#     Returns chunks with structure:
#     {
#         "content": "chunk text",
#         "test_name": "Test Name",
#         "category": "category from filename",
#         "content_type": "definition|normal_range|interpretation|note"
#     }
#     """
    
#     text = text.replace("\r", "\n")
    
#     # Extract test name from content
#     test_name = extract_test_name_from_content(text)
    
#     # Extract category from filename (e.g., "blood_sugar_test.txt" -> "blood_sugar")
#     category = filename.replace('.txt', '').strip()
    
#     chunks = []
    
#     # Split by major sections
#     section_pattern = r'\n(Test:|Purpose:|Types of Test:|Parameters:|Normal Ranges|Interpretation:|Note:|Preparation:)\s*\n'
#     sections = re.split(section_pattern, text)
    
#     i = 0
#     while i < len(sections):
#         if i + 1 >= len(sections):
#             break
            
#         section_header = sections[i].strip()
#         section_content = sections[i + 1].strip()
        
#         if not section_content:
#             i += 2
#             continue
        
#         # Determine content type and create chunks
#         if 'Normal Range' in section_header or 'Normal Ranges' in section_header:
#             # Split normal ranges into individual test parameters
#             lines = section_content.split('\n')
#             current_param = ""
            
#             for line in lines:
#                 line = line.strip()
#                 if not line:
#                     continue
                
#                 # Check if this is a new parameter line
#                 if line and not line.startswith('-') and ':' in line:
#                     if current_param:
#                         chunks.append({
#                             "content": current_param.strip(),
#                             "test_name": test_name,
#                             "category": category,
#                             "content_type": "normal_range"
#                         })
#                     current_param = line
#                 else:
#                     current_param += "\n" + line
            
#             if current_param:
#                 chunks.append({
#                     "content": current_param.strip(),
#                     "test_name": test_name,
#                     "category": category,
#                     "content_type": "normal_range"
#                 })
        
#         elif 'Interpretation' in section_header:
#             # Split interpretation into individual bullet points
#             lines = section_content.split('\n')
#             for line in lines:
#                 line = line.strip()
#                 if line and not line.startswith('-'):
#                     continue
#                 if line:
#                     chunks.append({
#                         "content": line.replace('-', '').strip(),
#                         "test_name": test_name,
#                         "category": category,
#                         "content_type": "interpretation"
#                     })
        
#         elif 'Parameters' in section_header or 'Types of Test' in section_header:
#             # Split parameters/types into individual items
#             lines = section_content.split('\n')
#             for line in lines:
#                 line = line.strip()
#                 if line and not line.startswith('-'):
#                     continue
#                 if line:
#                     chunks.append({
#                         "content": line.replace('-', '').strip(),
#                         "test_name": test_name,
#                         "category": category,
#                         "content_type": "parameter"
#                     })
        
#         else:
#             # For Purpose, Note, etc. - keep as single chunk
#             if len(section_content) > 30:
#                 content_type = section_header.lower().replace(':', '').strip()
#                 chunks.append({
#                     "content": section_content,
#                     "test_name": test_name,
#                     "category": category,
#                     "content_type": content_type
#                 })
        
#         i += 2
    
#     return chunks


# def semantic_chunk(text):
#     """Legacy function for backward compatibility."""
#     text = text.replace("\r", "\n")
    
#     sections = re.split(
#         r'\n(?=(Test:|Purpose:|Overview:|Description:|Parameters:|Normal Ranges|Interpretation:|Note:))',
#         text
#     )
    
#     chunks = []
#     current = ""
    
#     for part in sections:
#         part = part.strip()
        
#         if not part:
#             continue
        
#         if len(current) + len(part) < 1200:
#             current += "\n" + part
#         else:
#             chunks.append(current.strip())
#             current = part
    
#     if current:
#         chunks.append(current.strip())
    
#     return chunks

# ============================================
# chunking.py
# Flexible Medical Knowledge Chunking
# ============================================

# import re
# from typing import List, Dict

# # =========================================================
# # 1. CLEAN OCR TEXT
# # =========================================================

# def clean_text(text: str) -> str:
#     text = text.replace("\r", "\n")
#     text = text.replace("�", " ")
#     text = text.replace("•", " ")
#     text = text.replace("?", " ")

#     # remove noisy symbols but keep medical-safe punctuation
#     text = re.sub(r"[^\w\s\-/:%().,\n]", " ", text)

#     # normalize spaces
#     text = re.sub(r"\s+", " ", text)

#     return text.strip()


# # =========================================================
# # 2. CATEGORY DETECTION
# # =========================================================

# def normalize_category(filename: str) -> str:
#     filename = filename.lower()

#     mappings = {
#         "cbc": ["cbc", "blood", "hematology"],
#         "lft": ["liver", "lft"],
#         "kidney": ["kidney", "renal", "creatinine"],
#         "diabetes": ["diabetes", "glucose", "hba1c"],
#         "lipid": ["lipid", "cholesterol"],
#         "thyroid": ["thyroid", "tsh", "t3", "t4"],
#         "urine": ["urine", "urinalysis"],
#         "vitamin": ["vitamin", "b12", "folate"],
#     }

#     for cat, keys in mappings.items():
#         if any(k in filename for k in keys):
#             return cat

#     return "general"


# # =========================================================
# # 3. BETTER SECTION DETECTION (FIXED)
# # =========================================================

# SECTION_PATTERN = r"(Patient Details:|Test Name:|Purpose:|Overview:|Description:|Parameters:|Normal Range:|Reference Range:|Interpretation:|Conclusion:|Impression:|Notes?:|Preparation:)"

# def split_sections(text: str):
#     parts = re.split(SECTION_PATTERN, text, flags=re.IGNORECASE)

#     sections = []
#     current_section = "general"

#     for part in parts:
#         part = part.strip()
#         if not part:
#             continue

#         # detect section headers
#         if re.fullmatch(SECTION_PATTERN, part, flags=re.IGNORECASE):
#             current_section = part.replace(":", "").strip().lower()
#         else:
#             sections.append((current_section, part))

#     return sections


# # =========================================================
# # 4. REMOVE CONTEXT WINDOW (IMPORTANT FIX)
# # =========================================================
# # ❌ Context was making chunks noisy → REMOVE IT

# def chunk_medical_report(text: str, filename: str) -> List[Dict]:

#     text = clean_text(text)
#     category = normalize_category(filename)

#     sections = split_sections(text)

#     final_chunks = []

#     for i, (section, content) in enumerate(sections):

#         content = clean_text(content)

#         if len(content) < 50:
#             continue

#         # remove duplicate whitespace-heavy chunks
#         if content.count("Normal") > 10:
#             continue

#         final_chunks.append({
#             "content": content,
#             "metadata": {
#                 "chunk_id": i,
#                 "category": category,
#                 "section": section.lower(),
#                 "source_file": filename
#             }
#         })

#     return final_chunks


# import re
# from typing import List, Dict


# def clean_text(text: str) -> str:
#     text = text.replace("\r", "\n")
#     text = text.replace("�", " ")
#     text = text.replace("•", " ")
#     text = re.sub(r"[^\w\s\-/:%().,\n]", " ", text)
#     text = re.sub(r"\s+", " ", text)
#     return text.strip()


# def normalize_category(filename: str) -> str:
#     filename = filename.lower()

#     mappings = {
#         "cbc": ["cbc", "blood", "hematology"],
#         "lft": ["liver", "lft"],
#         "kidney": ["kidney", "renal", "creatinine"],
#         "diabetes": ["diabetes", "glucose", "hba1c"],
#         "lipid": ["lipid", "cholesterol"],
#         "thyroid": ["thyroid", "tsh", "t3", "t4"],
#         "urine": ["urine", "urinalysis"],
#         "vitamin": ["vitamin", "b12", "folate"],
#     }

#     for cat, keys in mappings.items():
#         if any(k in filename for k in keys):
#             return cat

#     return "general"


# SECTION_PATTERN = r"""
# (Patient Details:|
# Test Name:|
# Purpose:|
# Overview:|
# Description:|
# Parameters:|
# Normal Range:|
# Reference Range:|
# Interpretation:|
# Conclusion:|
# Impression:|
# Notes?:|
# Preparation:|
# GENERAL:)
# """


# def split_sections(text: str):
#     parts = re.split(SECTION_PATTERN, text, flags=re.IGNORECASE | re.VERBOSE)

#     sections = []
#     current_section = "general"

#     for part in parts:
#         part = part.strip()
#         if not part:
#             continue

#         if re.match(SECTION_PATTERN, part, flags=re.IGNORECASE | re.VERBOSE):
#             current_section = part.replace(":", "").strip().lower()
#         else:
#             sections.append((current_section, part))

#     return sections


# def merge_sections(sections):
#     merged = []
#     current_section = None
#     buffer = []

#     for sec, content in sections:
#         if sec != current_section:
#             if buffer:
#                 merged.append((current_section, " ".join(buffer)))
#             current_section = sec
#             buffer = [content]
#         else:
#             buffer.append(content)

#     if buffer:
#         merged.append((current_section, " ".join(buffer)))

#     return merged


# def chunk_medical_report(text: str, filename: str) -> List[Dict]:

#     text = clean_text(text)
#     category = normalize_category(filename)

#     sections = split_sections(text)
#     sections = merge_sections(sections)

#     final_chunks = []
#     seen = set()

#     for i, (section, content) in enumerate(sections):

#         content = clean_text(content)

#         if len(content) < 50:
#             continue

#         key = content[:200]
#         if key in seen:
#             continue
#         seen.add(key)

#         final_chunks.append({
#             "content": content,
#             "metadata": {
#                 "chunk_id": i,
#                 "category": category,
#                 "section": section,
#                 "source_file": filename
#             }
#         })

#     return final_chunks



import re
from typing import List, Dict

# ================================
# CLEAN TEXT
# ================================

def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = text.replace("�", " ")
    text = text.replace("•", " ")
    text = re.sub(r"[^\w\s\-/:%().,\n]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ================================
# CATEGORY DETECTION
# ================================

def normalize_category(text: str) -> str:
    text = text.lower()

    mappings = {
        "cbc": ["hemoglobin", "rbc", "wbc", "platelet", "mcv", "mch"],
        "lft": ["bilirubin", "sgpt", "sgot", "alt", "ast", "alp"],
        "kidney": ["creatinine", "urea", "bun", "uric"],
        "diabetes": ["glucose", "hba1c", "sugar"],
        "lipid": ["cholesterol", "hdl", "ldl", "triglyceride", "vldl"],
        "thyroid": ["tsh", "t3", "t4", "thyroid"],
        "urine": ["urine", "protein", "ketone"],
        "vitamin": ["vitamin", "b12", "d3", "folate"],
    }

    for cat, keys in mappings.items():
        if any(k in text for k in keys):
            return cat

    return "general"


# ================================
# TEST EXTRACTION (IMPORTANT)
# ================================

TEST_PATTERN = re.compile(
    r"([A-Za-z\s\-/()]+?)\s+([0-9.]+)\s*([a-zA-Z/%]*)\s+([0-9.<>\-\s]+)\s*([A-Za-z]+)",
    re.IGNORECASE
)


def extract_test_level_chunks(text: str, category: str, filename: str) -> List[Dict]:

    chunks = []

    matches = TEST_PATTERN.findall(text)

    for i, match in enumerate(matches):

        test_name = match[0].strip()
        value = match[1].strip()
        unit = match[2].strip()
        ref_range = match[3].strip()
        status = match[4].strip()

        content = f"""
Test: {test_name}
Value: {value} {unit}
Reference Range: {ref_range}
Status: {status}
Category: {category}
"""

        chunks.append({
            "content": content.strip(),
            "metadata": {
                "chunk_id": i,
                "test_name": test_name.lower(),
                "category": category,
                "source_file": filename,
                "type": "test_level"
            }
        })

    return chunks


# ================================
# SECTION CHUNKING (FALLBACK)
# ================================

def section_chunking(text: str, filename: str, category: str) -> List[Dict]:

    sections = re.split(r"\n{2,}", text)

    chunks = []

    for i, sec in enumerate(sections):

        sec = clean_text(sec)

        if len(sec) < 40:
            continue

        chunks.append({
            "content": sec,
            "metadata": {
                "chunk_id": i,
                "category": category,
                "source_file": filename,
                "type": "section"
            }
        })

    return chunks


# ================================
# MAIN FUNCTION (SMART ROUTER)
# ================================

def chunk_medical_report(text: str, filename: str) -> List[Dict]:

    text = clean_text(text)
    category = normalize_category(text)

    # STEP 1: Try test-level chunking (BEST)
    test_chunks = extract_test_level_chunks(text, category, filename)

    # STEP 2: fallback if OCR is messy
    if len(test_chunks) < 3:
        section_chunks = section_chunking(text, filename, category)
        return section_chunks

    return test_chunks