import PyPDF2
import re
import string
import os

path = r"C:/cv/Columbia.pdf"

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

    return make_printable(text).strip()


def find_email(text):
    pattern = "[^\s@]+@[^@\s]+\.[^@\s]+"

    return (re.findall(pattern, text))


def find_phone_number(text):
    pattern = "[\d\-\(\) ]{9,}"

    return (re.findall(pattern, text))


def find_years_range(line):
	pattern = re.compile("\d{4} ?-? ?\d{4}")
	if (pattern.search(line) is not None):
		return True

	return False


def other_section_detected(line):
	keywords = ["Education", "University", "Experience", "Qualification", "Positions", "Publications", "Skills"]

	for k in keywords:
		if k in line:
			return True

	return False


def separate_section(text):
	lines = text.splitlines()
	section = ""

	for line in lines:
		if (not other_section_detected(line) and not find_years_range(line)):
			section += line
		else:
			break

	return section


dir_list =(os.listdir("C:\\cv\\"))

for file in dir_list:
    print (file)
    print (find_email(pdf_to_str("C:\\cv\\"+ file)))
    print (20*"-")

print (pdf_to_str(path))
print (20*"-")
print (find_email(pdf_to_str(path)))
print (find_years_range(pdf_to_str(path)))
print (separate_section(pdf_to_str(path)))


