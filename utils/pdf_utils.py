from fpdf import FPDF
import os

class QuestionPDF(FPDF):
    """
    Custom PDF class for exporting questions
    """
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.set_font("Arial", size=12)
        
    def header(self):
        # Set header
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Question Paper", 0, 1, "C")
        self.ln(10)
        
    def footer(self):
        # Set footer
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        page_number = f"Page {self.page_no()}"
        self.cell(0, 10, page_number, 0, 0, "C")
        
    def add_question(self, question_num, question_text, options=None, language=None):
        """
        Add a question with its options to the PDF
        """
        if language and language != "English":
            self.set_font("Arial", "B", 10)
            self.cell(0, 10, f"Language: {language}", 0, 1)
        
        self.set_font("Arial", "B", 12)
        self.multi_cell(0, 10, f"{question_num}. {question_text}")
        self.ln(5)
        
        if options and len(options) > 0:
            self.set_font("Arial", "", 12)
            for option in options:
                self.multi_cell(0, 10, f"   {option}")
            self.ln(10)
        else:
            self.ln(10)

def export_questions_to_pdf(questions, filepath="questions.pdf"):
    """
    Export a list of questions to PDF
    
    Args:
        questions: List of question dictionaries with keys:
                  - question_text: The text of the question
                  - options: List of option strings
                  - language: Optional language indicator
        filepath: Path to save the PDF file
    """
    pdf = QuestionPDF()
    
    for i, q in enumerate(questions, 1):
        pdf.add_question(
            i, 
            q.get("question_text", ""),
            q.get("options", []),
            q.get("language", "English")
        )
    
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
    
    # Save PDF
    pdf.output(filepath)
    return filepath 