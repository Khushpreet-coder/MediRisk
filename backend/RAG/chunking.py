import re


# =====================================
# Semantic Chunking Function
# =====================================

def semantic_chunk(text):

    text = text.replace("\r", "\n")

    major_sections = re.split(
        r'\n(?=(Test:|Purpose:|Overview:|Description:|Parameters:|Normal Ranges|Interpretation:|Preparation:|Note:))',
        text
    )

    chunks = []

    current_chunk = ""

    for part in major_sections:

        part = part.strip()

        if not part:
            continue

        # Keep chunks meaningful size
        if len(current_chunk) + len(part) < 1000:

            current_chunk += "\n\n" + part

        else:

            chunks.append(current_chunk.strip())

            current_chunk = part

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks