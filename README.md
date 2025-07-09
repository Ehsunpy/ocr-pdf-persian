# OCR to PDF Converter

**Employment Task Project**: Persian OCR text extraction and PDF generation tool using FPDF with full Persian language support.

> **Note**: This project was developed as a text extraction task assigned to me for employment purposes. It demonstrates my skills in Python development, API integration, Persian text processing, and PDF generation.

## 🌟 Features

- **Persian Text Support**: Full support for Persian/Farsi text with proper RTL rendering
- **OCR Integration**: Automatic text extraction from PDF files using Alefba OCR API
- **Font Management**: Automatic detection and loading of Persian fonts (IRANSans)
- **PDF Generation**: Clean PDF reports with extracted text
- **Fallback Mode**: Works even without Persian fonts (with transliteration)
- **Batch Processing**: Process multiple PDF files simultaneously

## 📋 Requirements

- Python 3.7+
- Internet connection (for OCR API)
- Persian font file (IRANSans.ttf) in `fonts/` directory

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ocr-pdf-persian.git
cd ocr-pdf-persian

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup

1. **Add Persian Font**: Place `IRANSans.ttf` font file in the `fonts/` directory
2. **Add PDF Files**: Place your PDF files in the `pdfs/` directory
3. **API Configuration**: The tool uses Alefba OCR API (token included)

### 3. Usage

```bash
# Run the OCR and PDF generation process
python pdf_generator.py
```

The tool will:
1. 🔍 Find all PDF files in `pdfs/` directory
2. 📡 Send them to OCR API for text extraction
3. 📄 Generate a comprehensive PDF report
4. 💾 Save the result in `extracted_texts/ocr_results.pdf`

## 📁 Project Structure

```
ocr-pdf-persian/
├── pdf_generator.py          # Main application file
├── ocr_improved.py          # OCR API integration
├── requirements.txt         # Python dependencies
├── fonts/                   # Persian font files
│   └── IRANSans.ttf        # Persian font (not included)
├── pdfs/                    # Input PDF files
├── extracted_texts/         # Output directory
│   └── ocr_results.pdf     # Generated report
└── README.md               # This file
```

## 🔧 Configuration

### API Settings
The tool uses Alefba OCR API with the following settings:
- **Endpoint**: `https://alefba.roshan-ai.ir/api/read_document/`
- **Token**: Pre-configured (included in code)
- **Timeout**: 120 seconds per file

### Font Configuration
Supported font paths (searched in order):
1. `fonts/IRANSans.ttf`
2. `fonts/IranSans.ttf`
3. `fonts/IRANSans_Bold.ttf`
4. `fonts/IRANSans_Black.ttf`
5. `IRANSans.ttf` (root directory)

## 📖 Usage Examples

### Basic Usage
```bash
# Process all PDFs in pdfs/ directory
python pdf_generator.py
```

### Custom Processing
You can modify `pdf_generator.py` to:
- Change output filename
- Modify PDF formatting
- Add custom text processing
- Change API settings

## 🎨 PDF Output Features

- **Persian Headers/Footers**: Proper Persian text in headers and footers
- **RTL Text Alignment**: Right-to-left text alignment for Persian content
- **File Summary**: Overview of processed files and success rate
- **Character Count**: Shows extracted text length for each file
- **Page Breaks**: Separate page for each processed file
- **Error Handling**: Graceful handling of failed extractions

## 🔍 Technical Details

### Persian Text Processing
```python
# Text processing pipeline
reshaped_text = arabic_reshaper.reshape(text)
bidi_text = get_display(reshaped_text)
```

### Font Loading
```python
# Automatic font detection and loading
pdf.add_font('IRANSans', '', font_path)
pdf.set_font('IRANSans', '', font_size)
```

### OCR Integration
```python
# API call with proper headers
headers = {'Authorization': f'Token {token}'}
files = {'document': (filename, file_obj, 'application/pdf')}
response = requests.post(api_url, headers=headers, files=files)
```

## 🎯 Technical Skills Demonstrated

This employment task project showcases the following technical competencies:

### Programming & Development
- **Python Programming**: Object-oriented design, error handling, modular code structure
- **File I/O Operations**: Batch processing of PDF files, directory management
- **API Integration**: RESTful API consumption, HTTP requests with proper headers
- **Unicode & Text Processing**: Complex text manipulation for right-to-left languages

### Specialized Libraries & Tools
- **PDF Generation**: Custom FPDF implementation with Persian text support
- **Text Processing**: Arabic reshaper and bidirectional text algorithm implementation
- **Font Management**: Dynamic font loading and fallback mechanisms
- **HTTP Requests**: Robust API communication with timeout and error handling

### International Text Support
- **Persian/Farsi Language**: Full RTL text rendering and display
- **Arabic Reshaping**: Proper character joining and text shaping
- **Bidirectional Text**: Correct text direction handling for mixed content
- **Font Integration**: Custom font loading for non-Latin scripts

### Software Engineering Practices
- **Code Organization**: Clean, maintainable, and well-documented code
- **Error Handling**: Comprehensive exception management and user feedback
- **User Experience**: Clear console output with progress indicators and emojis
- **Documentation**: Bilingual documentation (English/Persian) with examples

## 🛠️ Dependencies

- **fpdf2**: PDF generation with Unicode support
- **arabic-reshaper**: Arabic/Persian text reshaping
- **python-bidi**: Bidirectional text algorithm
- **requests**: HTTP client for API calls

## 🐛 Troubleshooting

### Common Issues

1. **No Persian Font Found**
   - Download `IRANSans.ttf` and place in `fonts/` directory
   - Tool will work in fallback mode without Persian font

2. **API Connection Failed**
   - Check internet connection
   - Verify API endpoint is accessible

3. **PDF Processing Failed**
   - Ensure PDF files are not corrupted
   - Check file size (max 50MB recommended)

4. **Empty Output**
   - Verify PDF files contain extractable text
   - Check API response for errors

### Error Messages

- `❌ No Persian font found`: Place font file in `fonts/` directory
- `❌ Cannot connect to API`: Check internet connection
- `❌ Directory pdfs not found`: Create `pdfs/` directory and add PDF files

## 📄 License

This project was developed as an employment task to demonstrate technical skills in:
- Python programming and file handling
- API integration and HTTP requests
- Persian/Arabic text processing and bidirectional text
- PDF generation with Unicode support
- Error handling and user experience design

Feel free to use and modify according to your needs for educational or commercial purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review error messages in console output
3. Create an issue in the repository

---

**Note**: This tool requires an active internet connection for OCR processing. The Persian font file is not included due to licensing restrictions - please obtain `IRANSans.ttf` separately.
