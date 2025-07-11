import os
import datetime
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import arabic_reshaper
from bidi.algorithm import get_display

class PersianPDF(FPDF):
    """FPDF-based class with Persian text support"""

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.font_path = self.get_persian_font()
        if self.font_path:
            try:
                self.add_font('IRANSans', '', self.font_path)
                self.has_persian_font = True
            except:
                self.has_persian_font = False
        else:
            self.has_persian_font = False

    def process_persian_text(self, text):
        if not text or not text.strip():
            return ""
        try:
            reshaped = arabic_reshaper.reshape(text)
            return get_display(reshaped)
        except:
            return text

    def get_persian_font(self):
        fonts = [
            "fonts/IRANSans.ttf",
            "fonts/IranSans.ttf",
            "fonts/IRANSans_Bold.ttf",
            "fonts/IRANSans_Black.ttf",
            "IRANSans.ttf"
        ]
        for font in fonts:
            if os.path.exists(font):
                return font
        return None

    def header(self):
        self.set_font('IRANSans' if self.has_persian_font else 'Helvetica', '', 15)
        title = self.process_persian_text("نتایج استخراج OCR") if self.has_persian_font else "OCR Extraction Results"
        self.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('IRANSans' if self.has_persian_font else 'Helvetica', '', 8)
        page_text = self.process_persian_text(f"صفحه {self.page_no()}") if self.has_persian_font else f"Page {self.page_no()}"
        self.cell(0, 10, page_text, align='C')

    def split_text_to_lines(self, text, max_chars=80):
        lines = []
        paragraphs = text.split('\n')
        for para in paragraphs:
            if not para.strip():
                lines.append("")
                continue
            words = para.split()
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if len(test_line) > max_chars:
                    if current_line:
                        lines.append(current_line)
                        current_line = word
                    else:
                        lines.append(word[:max_chars])
                        current_line = word[max_chars:]
                else:
                    current_line = test_line
            if current_line:
                lines.append(current_line)
        return lines

    def add_persian_text(self, text, font_size=10):
        self.set_font('IRANSans' if self.has_persian_font else 'Helvetica', '', font_size)
        processed_text = self.process_persian_text(text) if self.has_persian_font else text
        align = 'R' if self.has_persian_font else 'L'
        for line in self.split_text_to_lines(processed_text):
            if line.strip():
                self.cell(0, 8, line, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align=align)
            else:
                self.ln(4)

    def create_pdf_report(self, extracted_texts, pdf_files, output_filename="ocr_results.pdf"):
        """Create a PDF report from extracted OCR texts"""
        if not os.path.exists("extracted_texts"):
            os.makedirs("extracted_texts")
        output_path = os.path.join("extracted_texts", output_filename)

        self.add_page()
        self.set_font('IRANSans' if self.has_persian_font else 'Helvetica', '', 16)
        title = self.process_persian_text(f"نتایج OCR - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") if self.has_persian_font else f"OCR Results - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        self.cell(0, 10, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        self.ln(10)

        total_files = len(pdf_files)
        successful = sum(1 for text in extracted_texts if text.strip())
        self.set_font('IRANSans' if self.has_persian_font else 'Helvetica', '', 12)
        self.cell(0, 8, self.process_persian_text(f"تعداد کل فایل‌ها: {total_files}") if self.has_persian_font else f"Total files: {total_files}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
        self.cell(0, 8, self.process_persian_text(f"استخراج موفق: {successful}") if self.has_persian_font else f"Successful: {successful}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
        self.ln(10)

        for i, (pdf_file, text) in enumerate(zip(pdf_files, extracted_texts)):
            file_name = os.path.basename(pdf_file)
            self.set_font('IRANSans' if self.has_persian_font else 'Helvetica', '', 14)
            title_line = self.process_persian_text(f"فایل {i+1}: {file_name}") if self.has_persian_font else f"File {i+1}: {file_name}"
            self.cell(0, 10, title_line, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
            self.ln(5)

            if text.strip():
                self.set_font('IRANSans' if self.has_persian_font else 'Helvetica', '', 10)
                char_count = self.process_persian_text(f"تعداد کاراکترها: {len(text)}") if self.has_persian_font else f"Characters: {len(text)}"
                self.cell(0, 6, char_count, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
                self.ln(5)
                self.add_persian_text(text, 10)
            else:
                self.set_font('IRANSans' if self.has_persian_font else 'Helvetica', '', 10)
                no_text = self.process_persian_text("هیچ متنی استخراج نشد") if self.has_persian_font else "No text extracted"
                self.cell(0, 8, no_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')

            if i < len(pdf_files) - 1:
                self.ln(10)
                self.add_page()

        try:
            self.output(output_path)
            print(f"✅ PDF report created: {output_path}")
            return output_path
        except Exception as e:
            print(f"❌ Error creating PDF report: {e}")
            return None
