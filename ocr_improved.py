import requests
import os
import json

def test_connection():
    """Test basic connection to the API"""
    try:
        response = requests.get("https://alefba.roshan-ai.ir", timeout=10)
        return response.status_code == 200
    except:
        return False

def ocr_pdfs(file_paths, api_url, token):
    """Process PDFs with OCR API using official Alefba documentation"""
    texts = []

    for file_path in file_paths:
        print(f"Processing: {file_path}")
        
        # Check file existence
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            texts.append("")
            continue
            
        # Check file size
        file_size = os.path.getsize(file_path)
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
                
                print(f"Sending request to API...")
                
                response = requests.post(
                    api_url, 
                    headers=headers, 
                    files=files,
                    timeout=120
                )

            if response.status_code == 200:
                try:
                    response_data = response.json()
                    
                    # Extract text from the official API response format
                    extracted_text = ""
                    
                    if 'pages' in response_data:
                        for page_num, page in enumerate(response_data['pages'], 1):
                            if 'text' in page:
                                page_text = page['text']
                                extracted_text += f"--- Page {page_num} ---\n{page_text}\n\n"
                            elif 'parts' in page:
                                for part in page['parts']:
                                    if part.get('type') == 'text' and 'text' in part:
                                        extracted_text += part['text'] + "\n"
                    
                    # Clean up the extracted text
                    extracted_text = extracted_text.strip()
                    texts.append(extracted_text)
                    
                    print(f"OCR successful: {file_path}")
                    
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
                    texts.append("")
            else:
                print(f"OCR error for file {file_path}: {response.status_code}")
                texts.append("")

        except requests.exceptions.Timeout:
            print(f"Request timeout for {file_path}")
            texts.append("")
        except requests.exceptions.ConnectionError:
            print(f"Network connection error for {file_path}")
            texts.append("")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            texts.append("")

    return texts

# Remove the main function since it's now handled by pdf_output_generator.py
