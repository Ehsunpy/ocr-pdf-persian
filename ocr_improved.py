import requests
import os
import json
import sys

def test_connection():
    """Test basic connection to the API"""
    api_url = "https://alefba.roshan-ai.ir/api/read_document/"
    token = "1d55fa5dfe5cfafdcd6b24fd6d516e7cdee7c4af"
    
    print("Testing API endpoint...")
    try:
        response = requests.get("https://alefba.roshan-ai.ir", timeout=10)
        print(f"Base URL accessible: {response.status_code}")
    except Exception as e:
        print(f"Cannot reach base URL: {e}")
        return False
    
    return True

def ocr_pdfs(file_paths, api_url, token):
    """Process PDFs with OCR API using official Alefba documentation"""
    texts = []

    for file_path in file_paths:
        print(f"\n Processing: {file_path}")
        
        # Check file existence
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            texts.append("")
            continue
            
        # Check file size
        file_size = os.path.getsize(file_path)
        print(f"File size: {file_size:,} bytes")
        
        if file_size > 50 * 1024 * 1024:  # 50MB
            print(f"Large file - may take longer to process")
            
        try:
            # Use the official API format from documentation
            headers = {
                'Authorization': f'Token {token}'
            }
            
            with open(file_path, 'rb') as f:
                files = {
                    'document': (os.path.basename(file_path), f, 'application/pdf')
                }
                
                print(f" Sending request to API...")
                
                response = requests.post(
                    api_url, 
                    headers=headers, 
                    files=files,
                    timeout=120  # Increased timeout
                )

            print(f" Response received - Status code: {response.status_code}")
            print(f" Headers: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    print(f" Response keys: {list(response_data.keys())}")
                    
                    # Extract text from the official API response format
                    # According to documentation, the response has 'pages' array
                    extracted_text = ""
                    
                    if 'pages' in response_data:
                        for page_num, page in enumerate(response_data['pages'], 1):
                            print(f" Processing page {page_num}")
                            
                            # Each page has a 'text' field with the complete page text
                            if 'text' in page:
                                page_text = page['text']
                                extracted_text += f"--- Page {page_num} ---\n{page_text}\n\n"
                            
                            # Alternative: Extract from parts structure if needed
                            elif 'parts' in page:
                                for part in page['parts']:
                                    if part.get('type') == 'text' and 'text' in part:
                                        extracted_text += part['text'] + "\n"
                    
                    # Clean up the extracted text
                    extracted_text = extracted_text.strip()
                    texts.append(extracted_text)
                    
                    print(f" OCR successful: {file_path}")
                    print(f" Extracted text length: {len(extracted_text)} characters")
                    
                    if extracted_text:
                        print(f" Text sample: {extracted_text[:200]}...")
                        # Print the full extracted text to console
                        print(f"\n Full extracted text for {file_path}:")
                        print("=" * 60)
                        print(extracted_text)
                        print("=" * 60)
                    else:
                        print(" No text content found in response")
                    
                except json.JSONDecodeError as e:
                    print(f" JSON parsing error: {e}")
                    print(f" Raw response (first 500 characters): {response.text[:500]}")
                    texts.append("")
            else:
                print(f" OCR error for file {file_path}")
                print(f" Error code: {response.status_code}")
                print(f"Error message: {response.text}")
                texts.append("")

        except requests.exceptions.Timeout:
            print(f" Error: Request timeout for {file_path} (more than 120 seconds)")
            texts.append("")
        except requests.exceptions.ConnectionError as e:
            print(f" Network connection error: {e}")
            texts.append("")
        except requests.exceptions.RequestException as e:
            print(f" Request error: {e}")
            texts.append("")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            texts.append("")

    return texts

def main():
    print(" Starting OCR process...")
    print(f" Python version: {sys.version}")
    
    # Check requests library
    try:
        import requests
        print(f" Requests version: {requests.__version__}")
    except ImportError:
        print(" Requests library not found. Please install it with: pip install requests")
        return
    
    # Test connection first
    if not test_connection():
        print("❌ Cannot connect to API. Please check your internet connection.")
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
        print(f"Found {len(pdf_files)} PDF files in {pdfs_dir} directory")
        for pdf_file in pdf_files:
            print(f"   - {pdf_file}")
    else:
        print(f"Directory {pdfs_dir} not found!")
        return

    print(f" API URL: {api_url}")
    print(f" Token: {token[:10]}...")
    print(f" Number of files: {len(pdf_files)}")

    results = ocr_pdfs(pdf_files, api_url, token)

    print("\n" + "="*50)
    print(" Final Results:")
    print("="*50)

    # Display texts
    for i, text in enumerate(results):
        print(f"\n File {pdf_files[i]}:")
        if text:
            print(f"Extracted text ({len(text)} characters):")
            print("-" * 40)
            print(text[:500] + "..." if len(text) > 500 else text)
        else:
            print("No text was extracted")
        print("-" * 40)

    # Save extracted texts to file
    output_dir = "extracted_texts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory {output_dir} created")

    for i, text in enumerate(results):
        if text:
            base_name = os.path.splitext(os.path.basename(pdf_files[i]))[0]
            output_file = os.path.join(output_dir, f"{base_name}.txt")
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Text saved: {output_file}")
            except Exception as e:
                print(f" Error saving file {output_file}: {e}")

    print("OCR process completed!")

if __name__ == "__main__":
    main()
