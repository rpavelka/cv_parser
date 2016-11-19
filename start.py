import PyPDF2
import re
import string

path = r"..\Columbia.pdf"

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
    for x in range(1):
        text +=  ((reader.getPage(x)).extractText())

    return make_printable(text)


def find_email(text):
    pattern = "[^\s@]+@[^@\s]+\.[^@\s]+"

    return (re.findall(pattern, text))

def find_years_range(text):
	pattern = "\d{4} ?-? ?\d{4}"
	return (re.findall(pattern, text))

def other_section_detected(line):
	keywords = ["Education", "University", "Experience"]

	for k in keywords:
		if k in line:
			return True

	return False

def separate_section(text):
	lines = text.splitlines()
	section = ""

	for line in lines:
		if (not other_section_detected(line)):
			section += line
		else:
			break

	return section




#print (pdf_to_str(path))
#print (20*"-")
#print (find_email(pdf_to_str(path)))
#print (find_years_range(pdf_to_str(path)))
print (separate_section(pdf_to_str(path)))

