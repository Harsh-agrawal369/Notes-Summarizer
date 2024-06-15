# Document Summarization Project

## Overview
This project facilitates document summarization by extracting text content from various sources including PDFs and image files. It leverages Optical Character Recognition (OCR) to handle different file formats and uses the llama 3 API via Groq Cloud for generating summaries.

## Features
- **PDF and Image Support:** Accepts PDF documents and image files (converted to PDF) for text extraction.
- **OCR Integration:** Utilizes `pdf2Img` and `easyOCR` libraries to extract text from images and PDFs.
- **Summarization:** Uses llama 3 API to generate concise summaries of the extracted text.
- **Downloadable Summaries:** Users can download the summarized document in PDF format for offline use.
- **Future Scope:** Plans to implement handwriting recognition for expanded functionality.

## Getting Started
Follow these steps to use the application:

1. **Upload:** Provide a PDF or image file with text content.
2. **Processing:** Files are converted to PDF (if necessary) and text is extracted using OCR.
3. **Summarize:** The extracted text is sent to llama 3 API for summarization.
4. **Download:** Retrieve and save the summarized document.

## Requirements
- Python 
- Dependencies:
  - `pdf2Img`
  - `easyOCR`


## Contact
For any inquiries or contributions, please reach out to the project contributors:

- **Harsh Agrawal**
  - Email: [harsh@example.com](mailto:harsh@example.com)

- **Shaurya Pratap Singh**
  - Email: [shaurya@example.com](mailto:shaurya@example.com)

### Project Status
This project is currently in progress. We welcome contributions and suggestions for improving the document summarization capabilities. Specifically, we are seeking assistance with implementing handwriting recognition features. If you have expertise or ideas in this area, please contact us.

Thank you for your interest and support!

