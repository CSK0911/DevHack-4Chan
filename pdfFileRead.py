import PyPDF2

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        # Use len(pdf_reader.pages) instead of pdf_reader.numPages
        for i in range(len(pdf_reader.pages)):
            pdf_page = pdf_reader.pages[i]  # Use the pages property to get the page
            text += pdf_page.extract_text()  # Use extract_text() instead of extractText()
    return text

# Example
file_path = 'Resume_JiaJean.pdf'
print(extract_text_from_pdf(file_path))
