import PyPDF2
import re

path = "C:\\cv\\Columbia.pdf"

def pdf_to_str(file):
    pdf = open(file, "rb")
    reader = PyPDF2.PdfFileReader(pdf)

    text = ""
    for x in range(reader.numPages):
        text +=  ((reader.getPage(x)).extractText())

    return text


def find_email(text):
    pattern = "[^\s@]+@[^@\s]+\.[^@\s]+"

    return (re.findall(pattern, text))


print (pdf_to_str(path))
print (20*"-")
print (find_email(pdf_to_str(path)))