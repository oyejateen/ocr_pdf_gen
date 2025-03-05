# Smart Question Manager

A Streamlit application for OCR-based question extraction, editing, multilingual translation, and PDF export.

## Demo


![Untitledvideo-MadewithClipchamp2](https://github.com/user-attachments/assets/d2ecb36b-95c9-4b0d-a6f8-f8ebe8877236)



## Features

1. **OCR-based Question Extraction**
   - Upload images containing text
   - AI extracts questions and answer options using Google Gemini

2. **Question Editing & Management**
   - Edit extracted questions and options
   - Add questions manually
   - Rearrange question sequence

3. **Multilingual Support**
   - Convert questions to various Indian regional languages
   - Powered by Google Gemini

4. **Export to PDF**
   - Export all questions to an editable PDF

## Setup

1. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install Tesseract OCR:
   - Windows: Download and install from [here](https://github.com/UB-Mannheim/tesseract/wiki)
   - Linux: `sudo apt install tesseract-ocr`
   - macOS: `brew install tesseract`

3. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```
   streamlit run app.py
   ```

## Usage

1. Upload an image with a question
2. Review and edit the extracted question
3. Add more questions manually if needed
4. Translate questions to desired languages
5. Export all questions to PDF

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
