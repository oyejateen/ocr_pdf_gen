import streamlit as st
import os
from PIL import Image
import time
from utils.ocr_utils import extract_questions_with_gemini, translate_text
from utils.pdf_utils import export_questions_to_pdf

st.set_page_config(
    page_title="Smart Question Manager",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.8rem;
        color: #0D47A1;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .question-box {
        background-color: #f0f2f6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "upload"
if "temp_question" not in st.session_state:
    st.session_state.temp_question = None
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False
if "edit_index" not in st.session_state:
    st.session_state.edit_index = -1

def add_question(question_text, options=None):
    """Add a new question to the session state"""
    if not options:
        options = []
    
    question = {
        "question_text": question_text,
        "options": options
    }
    
    if st.session_state.edit_mode and st.session_state.edit_index >= 0:
        
        st.session_state.questions[st.session_state.edit_index] = question
        st.session_state.edit_mode = False
        st.session_state.edit_index = -1
    else:
        
        st.session_state.questions.append(question)

def move_question(index, direction):
    """Move a question up or down in the list"""
    if direction == "up" and index > 0:
        st.session_state.questions[index], st.session_state.questions[index-1] = \
            st.session_state.questions[index-1], st.session_state.questions[index]
    elif direction == "down" and index < len(st.session_state.questions) - 1:
        st.session_state.questions[index], st.session_state.questions[index+1] = \
            st.session_state.questions[index+1], st.session_state.questions[index]

# App header
st.markdown('<p class="main-header">Smart Question Manager</p>', unsafe_allow_html=True)


if st.session_state.current_page == "upload":
    st.markdown("### Upload an image containing questions")
    
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Extract Question"):
            with st.spinner("Extracting question from image..."):
                
                extracted_text = extract_questions_with_gemini(image)
                
                lines = extracted_text.strip().split('\n')
                question_text = ""
                options = []
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line.lower().startswith("question:"):
                        question_text = line[9:].strip()
                    elif line[0].upper() in "ABCD" and len(line) > 1 and line[1] in ".)":
                        options.append(line)
                
                st.session_state.temp_question = {
                    "question_text": question_text,
                    "options": options
                }
        
        if st.session_state.temp_question:
            st.markdown("### Extracted Question")
            
            question_text = st.text_area(
                "Question Text",
                st.session_state.temp_question["question_text"],
                height=100
            )
            
            st.markdown("### Options")
            options = []
            for i in range(4):  # Always show 4 option fields
                option_letter = chr(65 + i)  # A, B, C, D
                default_value = ""
                if i < len(st.session_state.temp_question["options"]):
                    default_value = st.session_state.temp_question["options"][i]
                
                option_text = st.text_area(
                    f"Option {option_letter}",
                    default_value,
                    height=50,
                    key=f"option_{i}"
                )
                
                if option_text.strip():
                    if not option_text.startswith(f"{option_letter}."):
                        option_text = f"{option_letter}. {option_text}"
                    options.append(option_text)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Add Another Question"):
                    if question_text:
                        add_question(question_text, options)
                        st.session_state.temp_question = None
                        st.rerun()
                    else:
                        st.error("Question text cannot be empty.")
            
            with col2:
                if st.button("Save and Continue"):
                    if question_text:
                        add_question(question_text, options)
                        st.session_state.current_page = "manage"
                        st.rerun()
                    else:
                        st.error("Question text cannot be empty.")

elif st.session_state.current_page == "manage":
    st.markdown("### Manage Questions")
    
    if st.button("➕ Add New Question"):
        st.session_state.current_page = "upload"
        st.rerun()
    
    for i, question in enumerate(st.session_state.questions):
        with st.container():
            st.markdown(f'<div class="question-box">', unsafe_allow_html=True)
            
            col1, col2, col3, col4, col5 = st.columns([5, 1, 1, 1, 1])
            
            with col1:
                st.markdown(f"**Question {i+1}**")
            
            with col2:
                if st.button("Edit", key=f"edit_{i}"):
                    st.session_state.edit_mode = True
                    st.session_state.edit_index = i
            
            with col3:
                if st.button("Delete", key=f"delete_{i}"):
                    st.session_state.questions.pop(i)
                    st.rerun()
            
            with col4:
                if st.button("↑", key=f"up_{i}"):
                    move_question(i, "up")
                    st.rerun()
            
            with col5:
                if st.button("↓", key=f"down_{i}"):
                    move_question(i, "down")
                    st.rerun()
            
            if st.session_state.edit_mode and st.session_state.edit_index == i:
             
                edited_text = st.text_area(
                    "Question Text",
                    question["question_text"],
                    height=100,
                    key=f"edit_q_{i}"
                )
                
                edited_options = []
                for j in range(4):
                    option_letter = chr(65 + j)
                    default_value = ""
                    if j < len(question["options"]):
                        default_value = question["options"][j]
                    
                    option_text = st.text_area(
                        f"Option {option_letter}",
                        default_value,
                        height=50,
                        key=f"edit_opt_{i}_{j}"
                    )
                    
                    if option_text.strip():
                        if not option_text.startswith(f"{option_letter}."):
                            option_text = f"{option_letter}. {option_text}"
                        edited_options.append(option_text)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Save Changes", key=f"save_{i}"):
                        if edited_text:
                            add_question(edited_text, edited_options)
                            st.rerun()
                        else:
                            st.error("Question text cannot be empty.")
                
                with col2:
                    if st.button("Cancel", key=f"cancel_{i}"):
                        st.session_state.edit_mode = False
                        st.session_state.edit_index = -1
                        st.rerun()
            
            else:
                st.markdown(f"**Question:** {question['question_text']}")
                
                if question.get('options'):
                    st.markdown("**Options:**")
                    for option in question['options']:
                        st.markdown(f"- {option}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.questions:
        st.markdown("### Export to PDF")
        
        default_filename = f"questions_{time.strftime('%Y%m%d_%H%M%S')}.pdf"
        filename = st.text_input("Filename", default_filename)
        
        if st.button("Export to PDF"):
            with st.spinner("Generating PDF..."):
                try:
                    pdf_path = export_questions_to_pdf(st.session_state.questions, filename)
                    
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                    
                    st.success("PDF generated successfully!")
                    st.download_button(
                        label="Download PDF",
                        data=pdf_bytes,
                        file_name=filename,
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Smart Question Manager | Created with Streamlit and Google Gemini") 