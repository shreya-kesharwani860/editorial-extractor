import os
import json
from PyPDF2 import PdfReader
from llm_utils import summarize_text, extract_metadata

def extract_text_from_pdf(pdf_path):
    """Extract text from all pages of a PDF"""
    text = ""
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def process_editorials(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            raw_text = extract_text_from_pdf(pdf_path)

            # Save raw text
            raw_text_file = os.path.join(output_folder, filename.replace(".pdf", "_raw.txt"))
            with open(raw_text_file, "w", encoding="utf-8") as f:
                f.write(raw_text)

            # Save summary
            summary = summarize_text(raw_text)
            summary_file = os.path.join(output_folder, filename.replace(".pdf", "_summary.txt"))
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(summary)

            # Save metadata
            metadata = extract_metadata(raw_text)
            metadata_file = os.path.join(output_folder, filename.replace(".pdf", "_metadata.json"))
            with open(metadata_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=4)

if __name__ == "__main__":
    input_folder = "editorial_pages"        
    output_folder = "output_summaries"      

    process_editorials(input_folder, output_folder)
    print("✅ Processing complete! Raw text, summaries, and metadata saved.")
