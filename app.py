import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def create_pdf_from_text(text):
    writer = PdfWriter()
    reader = PdfReader()
    input_stream = BytesIO(text.encode('utf-8'))
    reader.stream = input_stream
    reader.numPages = 1
    writer.add_page(reader.pages[0])
    output_stream = BytesIO()
    writer.write(output_stream)
    return output_stream.getvalue()

def main():
    st.title("PDF Bewerk Webapp")
    uploaded_file = st.file_uploader("Upload een PDF-bestand", type="pdf")
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        st.text_area("PDF inhoud:", text, height=300)
        edited_text = st.text_area("Bewerk de tekst:", text, height=300)

        if st.button("Download gewijzigde PDF"):
            modified_pdf = create_pdf_from_text(edited_text)
            st.download_button(
                label="Download PDF",
                data=modified_pdf,
                file_name="gewijzigde_document.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
