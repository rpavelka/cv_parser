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
    for x in range(reader.numPages):
        text +=  ((reader.getPage(x)).extractText())

    return make_printable(text).strip()


def find_email(text):
    pattern = "[^\s@]+@[^@\s]+\.[^@\s]+"

    return (re.findall(pattern, text))

def find_phone_number(text):
    pattern = "[\d\-\(\) ]{9,}"

    return (re.findall(pattern, text))

print (pdf_to_str(path))

print (20*"-")
print (find_email(pdf_to_str(path)))
print (20*"-")
print (find_phone_number(pdf_to_str(path)))

dir_list =(os.listdir("C:\\cv\\"))

for file in dir_list:
    print (file)
    print (find_email(pdf_to_str("C:\\cv\\"+ file)))
    print (20*"-")




