# # RAG/text_normalizer.py

# def normalize_medical_text(text):

#     replacements = {
#         "�": "-",
#         "–": "-",
#         "—": "-",
#         "≤": "<=",
#         "≥": ">=",
#         "µ": "micro"
#     }

#     for old, new in replacements.items():
#         text = text.replace(old, new)

#     return text

def normalize_medical_text(text):

    replacements = {

        "�": "-",

        "–": "-",
        "—": "-",

        "≤": "<=",
        "≥": ">=",

        "µ": "micro",

        "\u00a0": " ",

        "\t": " "
    }

    for old, new in replacements.items():

        text = text.replace(old, new)

    # Remove extra spaces
    text = " ".join(text.split())

    return text