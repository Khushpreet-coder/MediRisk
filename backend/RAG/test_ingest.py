from ingestion import ingest_file
import fitz  # PyMuPDF

pdf_path = r"D:\Medical_Report_Summarizer - Copy\sterling-accuris-pathology-sample-report-unlocked-pages.pdf"


def extract_pdf_text(path):
    doc = fitz.open(path)
    text = ""

    for page in doc:
        text += page.get_text("text") + "\n"

    return text


if __name__ == "__main__":
    text = extract_pdf_text(pdf_path)

    print("PDF extracted. Length:", len(text))

    ingest_file(text, "cbc_report.txt")

    print("Ingestion complete")