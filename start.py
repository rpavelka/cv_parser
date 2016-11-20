#! /usr/bin/env python3
#-*- coding: utf-8 -*-

import re
import string
import os
import logging
import argparse
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine


logging.basicConfig(level=logging.ERROR)


def make_printable(text):
    result = ""
    for letter in text:
        if letter in string.printable:
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

    emails = ";".join(re.findall(pattern, text))

    return emails


def find_phone_number(text):
    pattern = "[\d\-\(\) \+]{9,}"

    result = (re.findall(pattern, text))
    final = []

    for number in result:
        number = number.strip()
        if not "  " in number:
            number = number.replace(" ", "")
            number = number.replace("-", "")
            if len(number) >= 9:
                final.append(number)

    return ";".join(final)


def find_name(text):
    pattern = r"[A-Z][a-z]{1,15}\.? ([A-Z][a-z]{0,15}\.? ?){0,3}[A-Z]\D{1,15}"

    return (re.findall(pattern, text))


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
            # if i < len(lines)-1:
            # 	result += lines[i + 1]

    return result


def other_section_detected(line):
    keywords = ["Education", "University", "Experience", "Qualification", "Positions", "Publications", "Skills"]

    for k in keywords:
        if k.lower() in line.lower():
            return True
    return False


def separate_section(text):
    lines = text.splitlines()
    section = ""

    for line in lines:
        if (not other_section_detected(line) and not find_years_range(line)):
            section += line + "\n"
        else:
            break

    return section


def create_resume_output(list_of_dict, file_name):
    header = []
    for row in list_of_dict:
        for k in row:
            if k not in header:
                header.append(k)
    data = []
    for row in list_of_dict:
        row_list= [row.get(x, "N/A") for x in header]
        row_list = [(i if i else "N/A") for i in row_list]
        data.append(row_list)



    return write_csv(data,header,file_name)


def write_csv(data, header, file_name):
    header = [str(s).replace("'","").replace(",","") for s in header]
    header = ['"{}"'.format(s) for s in header]
    clean_data = []
    for row in data:
        clean_data.append([str(s).replace("'","").replace(",","") for s in row])

    result = ",".join(header) + "\n"
    for row in clean_data:
        result += (",".join(['"{}"'.format(s) for s in row]))
        result += "\n"

    if not file_name:
        print (result)
    else:
        with open(file_name, "w") as f:
            f.write(result)


def main():
    parser = argparse.ArgumentParser(description='Script to parse PDF resumes, and create a csv file containing contact info')
    parser.add_argument('path_to_cvs', help='Path to file with pdf which include cvs.')
    parser.add_argument('--output_file_name','-o',default = None, help='Name of output file')

    args = parser.parse_args()
    input, output = args.path_to_cvs, args.output_file_name

    dir_list =(os.listdir(input))

    final_list = []

    for file in dir_list:
        cvs_dict = dict()
        pdf_text = pdf_to_str(input + file)
        #cvs_dict["name"] =  find_name(pdf_text)
        cvs_dict["email"] =  find_email(pdf_text)
        cvs_dict["phone_number"] =  find_phone_number(pdf_text)
        #cvs_dict["address"] = TODO
        #cvs_dict["last_education"] = TODO
        #cvs_dict["last_profession"] = TODO

        final_list.append(cvs_dict)

    create_resume_output(final_list, output)


if __name__ == "__main__":
    main()