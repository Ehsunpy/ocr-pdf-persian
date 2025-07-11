from ocr_improved import OcrApi
from pdf_generator import PersianPDF

def main():
    print("Starting OCR processing and PDF generation...")
    # Step 1: Extract text from PDFs
    ocr = OcrApi()
    ocr.find_pdfs()
    if not ocr.file_paths:
        print("No PDF files found.")
        return
    extracted_texts = ocr.ocr_pdfs()
    # Step 2: Generate PDF report with extracted texts
    pdf = PersianPDF()
    output_path = pdf.create_pdf_report(extracted_texts, ocr.file_paths)
    if output_path:
        print(f"PDF report successfully created: {output_path}")
    else:
        print("Error creating PDF report.")

if __name__ == "__main__":
    main()
