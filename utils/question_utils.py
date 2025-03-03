from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Google Generative AI
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

def structured_question_extraction(text):
    """
    Use LangChain and Google Gemini to parse raw OCR text into structured question and options
    """
    try:
        # Create the prompt template
        template = """
        You are a question extraction expert. Given the following raw text extracted from an image,
        extract the question and its options in a structured format.
        
        Raw text:
        {raw_text}
        
        Please format the output as follows:
        
        Question: [The question text]
        
        Options:
        A. [Option A]
        B. [Option B]
        C. [Option C]
        D. [Option D]
        
        If there are no options, just return the question.
        If the question or options are unclear, make your best guess.
        """
        
        # Create the prompt
        prompt = PromptTemplate(
            input_variables=["raw_text"],
            template=template,
        )
        
        # Initialize the LLM
        llm = ChatGoogleGenerativeAI(model="gemini-pro")
        
        # Create the chain
        chain = prompt | llm
        
        # Run the chain
        result = chain.invoke({"raw_text": text})
        
        # Return the structured result
        return result.content
    except Exception as e:
        return f"Error in structured extraction: {str(e)}"

def validate_question_format(question_dict):
    """
    Validate that the question dictionary has all the required fields
    """
    required_fields = ["question_text"]
    
    for field in required_fields:
        if field not in question_dict or not question_dict[field]:
            return False
    
    return True

def extract_from_structured_text(text):
    """
    Parse structured text from LLM into a question dictionary
    """
    result = {
        "question_text": "",
        "options": []
    }
    
    lines = text.strip().split("\n")
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.lower().startswith("question:"):
            current_section = "question"
            result["question_text"] = line[len("question:"):].strip()
        elif line.lower() == "options:":
            current_section = "options"
        elif current_section == "options" and line[0].upper() in "ABCD" and len(line) > 1 and line[1] in ".)":
            result["options"].append(line)
    
    return result 