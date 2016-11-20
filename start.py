import re
import string
import os
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
import logging




logging.basicConfig(level=logging.ERROR)




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

def find_name(text):
    #.*([A-Z]\D{1,15}\.?[ -](?:[A-Z]\D{0,15}\.? ?){0,3}[A-Z]\D{1,15})$
    pattern = r"\W*([A-Z][A-Za-z]*\.? (?:[A-Z][A-Za-z]*\.? ?){0,3}[A-Z][A-Za-z]*)\s?"
    name = re.findall(pattern, text)
    if name:
        return (name[0])
    else:
        return "N/A"


def find_years_range(line):
    pattern = re.compile("\d{4} ?-? ?\d{4}")
    if (pattern.search(line) is not None):
        return True

    return False

def find_year(line):
    pattern = re.compile(r" (19)|(20)\d{2}[ -]")
    if (pattern.search(line) is not None):
        return True

    return False


def find_jobs_and_education(text):
    lines = text.splitlines()
    result = ""

    for i, line in enumerate(lines):
        if find_year(line):
			# if i > 0:
			# 	result += lines[i-1]
            result += line + "\n"
            if i < len(lines)-1:
                result += lines[i + 1]

    return result

def other_section_detected(line):
    keywordsEducation = ["Education", "University", "Qualification", "Training", "Courses"]
    keywordsWork = ["Experience", "Positions", "Work", "Job", "Professional", "Profession"]
    keywordsOther = ["Publications", "Skills", "Reference"]

    for k in keywordsEducation:
        if k.lower() in line.lower():
            return "Education"

    for k in keywordsWork:
        if k.lower() in line.lower():
            return "Work"

    for k in keywordsOther:
        if k.lower() in line.lower():
            return "Other"

    return False


def separate_section(text):
    lines = text.splitlines()
    sections = {}
    currentSectionName = "ContactInformation"
    currentSectionContent = ""

    for line in lines:
        if (other_section_detected(line)):
            sections[currentSectionName] = currentSectionContent
            currentSectionContent = ""
            currentSectionName = other_section_detected(line)
            currentSectionContent += line + "\n"
        else:
            currentSectionContent += line + "\n"

    return sections

path = "C:\\Sallyino\\novy_parser\\zivotopisy\\"
dir_list =(os.listdir(path))
#dir_list = [r"C:\Sallyino\novy_parser\zivotopisy\LSE5.pdf"]
for file in dir_list:

    pdfText = pdf_to_str(path + file)
    SectionsDictionary = separate_section(pdfText)
    # print (separate_section(pdfText))
    # section = (separate_section(pdfText))
    # #print (section)
    print ("name: ")
    print (find_name(SectionsDictionary['ContactInformation']))
    print ("email: ")
    print (find_email(SectionsDictionary['ContactInformation']))
    print ("phone: ")
    print (find_phone_number(SectionsDictionary['ContactInformation']))
    #print (find_jobs_and_education(pdfText))
    print ("###########################")
    # print (file)
    # print (find_email(pdf_to_str("C:\\cv\\"+ file)))
    # print (20*"-")

# print (pdf_to_str(path))
# print (20*"-")
# print (find_email(pdf_to_str(path)))
# print (find_years_range(pdf_to_str(path)))
#print (separate_section(pdf_to_str(path)))
