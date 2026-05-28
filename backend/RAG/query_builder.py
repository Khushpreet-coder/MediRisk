# from typing import List, Dict


# def extract_abnormal_findings(structured_data: Dict) -> List[Dict]:
#     """
#     Extract ONLY abnormal test findings from structured data.
    
#     Returns tests that are NOT normal/optimal.
    
#     Args:
#         structured_data: Dict with "tests" list containing {test_name, status, value, ...}
    
#     Returns:
#         List of abnormal test dicts
#     """
    
#     tests = structured_data.get("tests", [])
    
#     abnormal_tests = []
    
#     ignore_status = ["normal", "optimal", "", None]
    
#     for test in tests:
#         status = test.get("status", "").strip().lower()
        
#         # Only include tests that are NOT normal
#         if status not in ignore_status:
#             abnormal_tests.append(test)
    
#     return abnormal_tests


# def build_abnormal_findings_query(structured_data: Dict) -> str:
#     """
#     Build a concise query from ONLY abnormal findings.
    
#     Example output:
#     "LYMPHOCYTE Low MONOCYTES Low MCHC High"
    
#     This replaces querying on the full OCR text.
    
#     Args:
#         structured_data: Structured test data
    
#     Returns:
#         Query string from abnormal findings
#     """
    
#     abnormal_tests = extract_abnormal_findings(structured_data)
    
#     if not abnormal_tests:
#         return ""
    
#     # Build query from abnormal test names and status
#     query_parts = []
    
#     for test in abnormal_tests:
#         test_name = test.get("test_name", "").strip()
#         status = test.get("status", "").strip()
        
#         if test_name:
#             query_parts.append(test_name)
        
#         if status:
#             query_parts.append(status)
    
#     return " ".join(query_parts)


# def build_category_filtered_queries(structured_data: Dict) -> List[Dict]:
#     """
#     Build multiple category-filtered queries from abnormal findings.
    
#     Returns queries with associated test categories for metadata filtering.
    
#     Example return:
#     [
#         {"query": "LYMPHOCYTE Low", "category": "cbc", "test_name": "LYMPHOCYTE"},
#         {"query": "MCHC High", "category": "cbc", "test_name": "MCHC"}
#     ]
    
#     Args:
#         structured_data: Dict with structured tests
    
#     Returns:
#         List of query dicts with category and test_name for filtering
#     """
    
#     abnormal_tests = extract_abnormal_findings(structured_data)
    
#     if not abnormal_tests:
#         return []
    
#     # Map test names to categories (common test groupings)
#     # This should match your knowledge base categories
#     test_to_category = {
#         # CBC Tests
#         "hemoglobin": "blood_sugar_test",  # Or detect from report
#         "hematocrit": "blood_sugar_test",
#         "wbc": "blood_sugar_test",
#         "rbc": "blood_sugar_test",
#         "lymphocyte": "blood_sugar_test",
#         "monocytes": "blood_sugar_test",
#         "neutrophils": "blood_sugar_test",
#         "mchc": "blood_sugar_test",
#         "platelets": "blood_sugar_test",
        
#         # LFT Tests
#         "bilirubin": "liver_function_test",
#         "sgot": "liver_function_test",
#         "sgpt": "liver_function_test",
#         "alkaline phosphatase": "liver_function_test",
#         "albumin": "liver_function_test",
        
#         # Kidney Tests
#         "creatinine": "kidney_test_explanation",
#         "urea": "kidney_test_explanation",
#         "bun": "kidney_test_explanation",
        
#         # Blood Sugar
#         "glucose": "blood_sugar_test",
#         "fasting glucose": "blood_sugar_test",
#         "random glucose": "blood_sugar_test",
        
#         # Lipid Profile
#         "cholesterol": "lipid_profile",
#         "triglycerides": "lipid_profile",
#         "hdl": "lipid_profile",
#         "ldl": "lipid_profile",
        
#         # Thyroid
#         "tsh": "Thyroid_Profile",
#         "t3": "Thyroid_Profile",
#         "t4": "Thyroid_Profile",
        
#         # Vitamins
#         "b12": "vitamin_profile",
#         "folic acid": "vitamin_profile",
#         "vitamin d": "vitamin_profile",
        
#         # Urine
#         "protein": "urine_analysis",
#         "glucose": "urine_analysis",
#         "wbc urine": "urine_analysis",
#         "rbc urine": "urine_analysis",
#     }
    
#     queries = []
    
#     for test in abnormal_tests:
#         test_name = test.get("test_name", "").strip()
#         status = test.get("status", "").strip()
        
#         if not test_name:
#             continue
        
#         # Build query
#         query = f"{test_name} {status}".strip()
        
#         # Try to determine category
#         category = test_to_category.get(test_name.lower(), "blood_sugar_test")
        
#         queries.append({
#             "query": query,
#             "category": category,
#             "test_name": test_name
#         })
    
#     return queries


# def build_queries(structured_data: Dict) -> List[Dict]:
#     """
#     Legacy wrapper for backward compatibility.
    
#     Args:
#         structured_data: Structured test data
    
#     Returns:
#         List of query dicts
#     """
#     return build_category_filtered_queries(structured_data)

# ============================================
# query_builder.py
# ============================================

from typing import Dict, List


def extract_abnormal_tests(structured_data: Dict):

    tests = structured_data.get("tests", [])

    abnormal = []

    ignore = ["normal", None]

    for test in tests:

        status = test.get("status", "").strip().lower()

        if status not in ignore:

            abnormal.append(test)

    return abnormal


def detect_category(test_name: str) -> str:

    test_name = test_name.lower()

    category_map = {

        "cbc": [
            "hemoglobin",
            "rbc",
            "wbc",
            "mcv",
            "mch",
            "mchc",
            "platelet",
            "lymphocyte",
            "monocyte",
            "neutrophil",
            "eosinophil",
            "basophil",
            "blood count",
            "hematocrit"
        ],

        "lft": [
            "bilirubin",
            "sgpt",
            "sgot",
            "alp",
            "albumin",
            "liver",
            "alkaline phosphatase",
            "globulin"
        ],

        "kidney": [
            "creatinine",
            "urea",
            "bun",
            "gfr",
            "kidney",
            "renal",
            "uric acid"
        ],

        "diabetes": [
            "glucose",
            "sugar",
            "hba1c",
            "insulin"
        ],

        "lipid": [
            "cholesterol",
            "hdl",
            "ldl",
            "triglyceride",
            "lipid",
            "vldl"
        ],

        "thyroid": [
            "thyroid",
            "tsh",
            "t3",
            "t4",
            "thyroglobulin"
        ],

        "urine": [
            "urine",
            "urinalysis",
            "specific gravity",
            "ketone",
            "nitrite",
            "urobilinogen",
            "microalbumin",
            "protein urine"
        ],

        "vitamin": [
            "vitamin",
            "b12",
            "folate",
            "folic acid",
            "d3",
            "calcium",
            "iron",
            "ferritin"
        ]
    }

    for category, keywords in category_map.items():

        for keyword in keywords:

            if keyword in test_name:
                return category

    return "general"


def build_rag_queries(structured_data):
    queries = []

    for test in structured_data.get("tests", []):
        test_name = test.get("test_name", "").strip()

        if not test_name:
            continue

        queries.append({
    "query": test_name,
    "category": detect_category(test_name)
})

    return queries