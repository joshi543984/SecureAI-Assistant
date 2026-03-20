from PyPDF2 import PdfReader

def read_pdf(file):
    try:
        text = ""
        reader = PdfReader(file)

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        return text
    except Exception as e:
        print("PDF Error:", e)
        return ""