
import streamlit as st
from fpdf import FPDF
import tempfile
from spellchecker import SpellChecker

# Initialize the spell checker
spell = SpellChecker()

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Personalized CV', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Helper function to create and download PDF

def create_pdf(name, description, skills, image):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, name, 0, 1, 'C')

    if image:
        pdf.image(image, x=10, y=30, w=50)

    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, f"Description: {description}")
    pdf.multi_cell(0, 10, f"Skills: {', '.join(skills)}")

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        pdf.output(tmp_file.name)
        return tmp_file.name

# Streamlit app
st.set_page_config(page_title="CV Maker", layout="wide")
st.title("CV Maker")

# Upload section
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Text inputs
name = st.text_input("Name")
description = st.text_area("Description")
skills = st.text_input("Skills (comma-separated)")

# Spell check
description_words = description.split()
incorrect_words = spell.unknown(description_words)
if incorrect_words:
    st.warning(f"Potential spelling mistakes: {', '.join(incorrect_words)}")

# Generate PDF
if st.button("Create PDF"):
    pdf_file = create_pdf(name, description, skills.split(','), uploaded_image)
    with open(pdf_file, "rb") as file:
        st.download_button(
            label="Download CV",
            data=file,
            file_name="cv.pdf",
            mime="application/pdf"
        )
