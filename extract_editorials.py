import zipfile
import os
from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfWriter, PdfReader

# ---------- CONFIG ----------
ZIP_FILE = "grid.zip"          # Your ZIP file
EXTRACT_DIR = "extracted_pdfs"
EDITORIAL_DIR = "editorial_pages"
MERGED_FILE = "merged_editorials.pdf"
DPI = 100                      # Lower DPI to speed up conversion
KEYWORDS = ["Editorial", "Opinion"]  # Keywords to detect pages
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update path if different
# ----------------------------

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

os.makedirs(EXTRACT_DIR, exist_ok=True)
os.makedirs(EDITORIAL_DIR, exist_ok=True)

# 1️⃣ Extract ZIP
with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_DIR)
print(f"[INFO] Extracted ZIP to {EXTRACT_DIR}")

# 2️⃣ Loop through PDFs
pdf_files = [os.path.join(EXTRACT_DIR, f) for f in os.listdir(EXTRACT_DIR) if f.lower().endswith(".pdf")]
for pdf_file in pdf_files:
    print(f"[INFO] Processing {pdf_file}")
    try:
        reader = PdfReader(pdf_file)
        writer = PdfWriter()
        for i in range(len(reader.pages)):
            try:
                images = convert_from_path(pdf_file, dpi=DPI, first_page=i+1, last_page=i+1)
                page_text = ""
                for img in images:
                    page_text += pytesseract.image_to_string(img)
                # Check if keywords exist
                if any(k.lower() in page_text.lower() for k in KEYWORDS):
                    writer.add_page(reader.pages[i])
            except Exception as e:
                print(f"[WARN] Skipping page {i+1} due to error: {e}")
        # Save editorial pages for this PDF
        if len(writer.pages) > 0:
            base_name = os.path.splitext(os.path.basename(pdf_file))[0]
            out_path = os.path.join(EDITORIAL_DIR, f"{base_name}_editorial.pdf")
            with open(out_path, "wb") as f:
                writer.write(f)
            print(f"[INFO] Extracted editorial pages to {out_path}")
    except Exception as e:
        print(f"[ERROR] Failed to process {pdf_file}: {e}")

# 3️⃣ Merge all editorial PDFs
merged_writer = PdfWriter()
editorial_pdfs = [os.path.join(EDITORIAL_DIR, f) for f in os.listdir(EDITORIAL_DIR) if f.endswith(".pdf")]
for pdf in editorial_pdfs:
    reader = PdfReader(pdf)
    for page in reader.pages:
        merged_writer.add_page(page)

with open(MERGED_FILE, "wb") as f:
    merged_writer.write(f)
print(f"[INFO] Merged all editorials into {MERGED_FILE}")
