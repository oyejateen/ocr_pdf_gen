import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_questions_with_gemini(image):
    """
    Use Google Gemini to extract questions and options from an image
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = """
        Extract the question and answer options from this image. 
        Format the output as follows:
        
        Question: [The question text]
        
        Options:
        A. [Option A]
        B. [Option B]
        C. [Option C]
        D. [Option D]
        
        If there are no options, just return the question.
        """
        
        response = model.generate_content([prompt, image])
        return response.text
    except Exception as e:
        return f"Error using Gemini for extraction: {str(e)}"

def translate_text(text, target_language):
    """
    Translate text to the target language using Google Gemini
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Translate the following text to {target_language}:
        
        {text}
        
        Preserve the exact format including any question numbers, options (A, B, C, D), 
        and other formatting elements.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error translating text: {str(e)}"

def parse_question_text(text):
    """
    Parse the extracted text to separate question from options
    """
    lines = text.strip().split('\n')
    question = ""
    options = []
    
    option_started = False
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith(('A.', 'B.', 'C.', 'D.', 'a.', 'b.', 'c.', 'd.', 'A)', 'B)', 'C)', 'D)')):
            option_started = True
            options.append(line)
        elif not option_started:
            if question:
                question += " " + line
            else:
                question = line
    
    return {
        "question": question,
        "options": options
    } 