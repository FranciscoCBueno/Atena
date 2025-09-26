import PyPDF2

#Extrair o texto de um txt
def extract_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
#Extrair o texto de um pdf
def extract_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text