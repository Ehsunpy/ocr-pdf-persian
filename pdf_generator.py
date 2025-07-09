import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import datetime
import arabic_reshaper
from bidi.algorithm import get_display
from ocr_improved import ocr_pdfs, test_connection

def process_persian_text(text):
    """Process Persian/Arabic text for proper rendering in PDF"""
    if not text or not text.strip():
        return ""
    
    try:
        # Reshape Arabic/Persian text
        reshaped_text = arabic_reshaper.reshape(text)
        # Apply bidirectional algorithm
        bidi_text = get_display(reshaped_text)
        return bidi_text
    except Exception as e:
        print(f"Warning: Text processing failed: {e}")
        return text

def get_persian_font():
    """Get Persian font from local fonts folder"""
    font_paths = [
        "fonts/IRANSans.ttf",
        "fonts/IranSans.ttf", 
        "fonts/IRANSans_Bold.ttf",
        "fonts/IRANSans_Black.ttf",
        "IRANSans.ttf"  # fallback in current directory
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            print(f"Persian font found: {font_path}")
            return font_path
    
    print("❌ No Persian font found - using fallback mode")
    return None

class PersianPDF(FPDF):
    """Custom FPDF class with Persian text support"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.setup_persian_font()
        
    def setup_persian_font(self):
        """Setup Persian font"""
        self.font_path = get_persian_font()
        if self.font_path:
            try:
                self.add_font('IRANSans', '', self.font_path)
                self.has_persian_font = True
                print(" Persian font loaded successfully")
            except Exception as e:
                print(f" Error loading Persian font: {e}")
                self.has_persian_font = False
        else:
            self.has_persian_font = False
        
    def header(self):
        """Add header to each page"""
        if self.has_persian_font:
            self.set_font('IRANSans', '', 15)
            header_text = process_persian_text('نتایج استخراج OCR')
            self.cell(0, 10, header_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        else:
            self.set_font('Helvetica', 'B', 15)
            self.cell(0, 10, 'OCR Extraction Results', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(10)
        
    def footer(self):
        """Add footer to each page"""
        self.set_y(-15)
        if self.has_persian_font:
            self.set_font('IRANSans', '', 8)
            footer_text = process_persian_text(f'صفحه {self.page_no()}')
            self.cell(0, 10, footer_text, align='C')
        else:
            self.set_font('Helvetica', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', align='C')
        
    def add_persian_text(self, text, font_size=10):
        """Add text with proper formatting - direct from OCR"""
        if self.has_persian_font:
            self.set_font('IRANSans', '', font_size)
            # Process text for Persian rendering
            processed_text = process_persian_text(text)
            align = 'R'  # Right align for Persian
        else:
            self.set_font('Helvetica', '', font_size)
            # No translation - use OCR text directly
            processed_text = text
            align = 'L'  # Left align for original text
        
        # Split text into manageable chunks
        lines = self.split_text_to_lines(processed_text)
        
        for line in lines:
            if line.strip():
                try:
                    self.cell(0, 8, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align=align)
                except Exception as e:
                    print(f"Error adding line: {e}")
                    # Final fallback - show simple message
                    self.set_font('Helvetica', '', font_size)
                    self.cell(0, 8, "[OCR text - encoding issue]", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
            else:
                self.ln(4)
                
    def split_text_to_lines(self, text, max_chars=80):
        """Split text into lines with reasonable length"""
        lines = []
        paragraphs = text.split('\n')
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                lines.append("")
                continue
                
            words = paragraph.split()
            current_line = ""
            
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if len(test_line) > max_chars:
                    if current_line:
                        lines.append(current_line)
                        current_line = word
                    else:
                        # Word is too long, split it
                        lines.append(word[:max_chars])
                        current_line = word[max_chars:]
                else:
                    current_line = test_line
                    
            if current_line:
                lines.append(current_line)
                
        return lines

def create_pdf_report(extracted_texts, pdf_files, output_filename="ocr_results.pdf"):
    """Create a PDF report with all extracted texts using FPDF"""
    
    # Create output directory if it doesn't exist
    output_dir = "extracted_texts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, output_filename)
    
    # Create PDF document
    pdf = PersianPDF()
    pdf.add_page()
    
    # Add title and summary
    if pdf.has_persian_font:
        pdf.set_font('IRANSans', '', 16)
        title_text = process_persian_text(f"نتایج OCR - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        pdf.cell(0, 10, title_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    else:
        pdf.set_font('Helvetica', 'B', 16)
        title = f"OCR Results - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        pdf.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(10)
    
    # Add summary
    total_files = len(pdf_files)
    successful_extractions = sum(1 for text in extracted_texts if text.strip())
    
    if pdf.has_persian_font:
        pdf.set_font('IRANSans', '', 12)
        summary_text = process_persian_text(f"تعداد کل فایل‌ها: {total_files}")
        pdf.cell(0, 8, summary_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
        summary_text2 = process_persian_text(f"استخراج موفق: {successful_extractions}")
        pdf.cell(0, 8, summary_text2, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
    else:
        pdf.set_font('Helvetica', '', 12)
        pdf.cell(0, 8, f"Total files processed: {total_files}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        pdf.cell(0, 8, f"Successful extractions: {successful_extractions}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
    pdf.ln(10)
    
    # Add extracted texts
    for i, (pdf_file, text) in enumerate(zip(pdf_files, extracted_texts)):
        # File title
        file_name = os.path.basename(pdf_file)
        
        if pdf.has_persian_font:
            pdf.set_font('IRANSans', '', 14)
            file_title = process_persian_text(f"فایل {i+1}: {file_name}")
            pdf.cell(0, 10, file_title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
        else:
            pdf.set_font('Helvetica', 'B', 14)
            try:
                display_name = f"File {i+1}: {file_name}"
                pdf.cell(0, 10, display_name, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
            except:
                pdf.cell(0, 10, f"File {i+1}: [Persian filename]", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        
        pdf.ln(5)
        
        if text.strip():
            # Add character count
            if pdf.has_persian_font:
                pdf.set_font('IRANSans', '', 10)
                char_info = process_persian_text(f"تعداد کاراکترها: {len(text)}")
                pdf.cell(0, 6, char_info, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
            else:
                pdf.set_font('Helvetica', 'I', 10)
                pdf.cell(0, 6, f"Characters extracted: {len(text)}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
            pdf.ln(5)
            
            # Add the extracted text
            pdf.add_persian_text(text, 10)
        else:
            if pdf.has_persian_font:
                pdf.set_font('IRANSans', '', 10)
                no_text_msg = process_persian_text("هیچ متنی از این فایل استخراج نشد")
                pdf.cell(0, 8, no_text_msg, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
            else:
                pdf.set_font('Helvetica', '', 10)
                pdf.cell(0, 8, "No text was extracted from this file", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        
        # Add space between files
        if i < len(pdf_files) - 1:
            pdf.ln(10)
            pdf.add_page()
    
    # Save the PDF
    try:
        pdf.output(output_path)
        print(f"PDF report created successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f" Error creating PDF report: {e}")
        return None

def main():
    """Main function to run OCR and generate PDF report"""
    print(" Starting OCR to PDF process...")
    
    # Test connection first
    if not test_connection():
        print(" Cannot connect to API. Please check your internet connection.")
        return
    
    api_url = "https://alefba.roshan-ai.ir/api/read_document/"
    token = "1d55fa5dfe5cfafdcd6b24fd6d516e7cdee7c4af"
    
    # Automatically find all PDF files in the pdfs directory
    pdfs_dir = "pdfs"
    pdf_files = []
    
    if os.path.exists(pdfs_dir):
        for filename in os.listdir(pdfs_dir):
            if filename.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(pdfs_dir, filename))
        print(f" Found {len(pdf_files)} PDF files in {pdfs_dir} directory")
    else:
        print(f" Directory {pdfs_dir} not found!")
        return
    
    if not pdf_files:
        print(" No PDF files found in the pdfs directory!")
        return
    
    # Process PDFs with OCR
    print(" Starting OCR processing...")
    extracted_texts = ocr_pdfs(pdf_files, api_url, token)
    
    # Create PDF report
    print(" PDF report...")
    output_file = create_pdf_report(extracted_texts, pdf_files)
    
    if output_file:
        print(f" Process completed! PDF report saved as: {output_file}")
    else:
        print(" Failed to create PDF report!")

if __name__ == "__main__":
    main()
