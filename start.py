import re
import string
import os
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
import logging

logging.basicConfig(level=logging.ERROR)

path = r"C:/cv/CV24.pdf"

def make_printable(text):
    result = ""
    for letter in text:
        if (letter in string.printable):
            result += letter
    return result


def pdf_to_str(file):
    fp = open(file, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    text = ""
    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                text += lt_obj.get_text()

    return make_printable(text).strip()


def find_email(text):
    pattern = "[^\s@]+@[^@\s]+\.[^@\s]+"

    return (re.findall(pattern, text))


def find_phone_number(text):
    pattern = "[\d\-\(\) \+]{9,}"

    result = (re.findall(pattern, text))
    final = []

    for number in result:
        print (number)
        number = number.strip()
        if not "  " in number:
            print (number)
            number = number.replace(" ", "")
            print (number)
            number = number.replace("-", "")
            print (number)
            if len(number) >= 9:
                final.append(number)

    return final


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
    print (separate_section(pdf_to_str("C:\\cv\\"+ file)))
    print (20*"-")

print (pdf_to_str(path))
print (20*"-")
print (find_email(pdf_to_str(path)))
print (find_years_range(pdf_to_str(path)))
