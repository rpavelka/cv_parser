import PyPDF2
import re
import string

path = r"C:\Sallyino\CVParser\Columbia.pdf"

def make_printable(text):
	result = ""
	for letter in text:
		if (letter in string.printable):
			result += letter
	return result

def pdf_to_str(file):
    pdf = open(file, "rb")
    reader = PyPDF2.PdfFileReader(pdf)

    text = ""
    for x in range(reader.numPages):
        text +=  ((reader.getPage(x)).extractText())

    return make_printable(text)


def find_email(text):
    pattern = "[^\s@]+@[^@\s]+\.[^@\s]+"

    return (re.findall(pattern, text))


print (pdf_to_str(path))
print (20*"-")
print (find_email(pdf_to_str(path)))
