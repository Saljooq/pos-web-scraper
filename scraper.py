#!/usr/bin/python3
from typing import List, Tuple
from urllib.request import urlopen
import re
import os
import sys
import html as htmllib
from html.parser import HTMLParser
from classes import Course, CustomParse

OUTPUT_FILE = "classes_3.csv"

def main():

    if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)

    file_ptr = open(OUTPUT_FILE, "a")

    url = "https://catalog.iastate.edu/azcourses/com_s/"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")


    parser = CustomParse()

    parser.feed(html)

    list_courses = parser.get_course_list()

    print(f"list size {len(list_courses)}\n")

    # writing the headers of the file
    file_ptr.write("dept,course_num,title,credit_info,requirement,description\n")


    for i, crse in enumerate(list_courses):
        title_temp = crse.title.split(':')
        temp_course_code_and_dept = sanitize_text(title_temp[0]).split()
        crse.course_code = temp_course_code_and_dept.pop(-1)
        crse.department = " ".join(temp_course_code_and_dept)

        crse.title = title_temp[1]
        file_ptr.write(csv_row_formatter(crse))


    file_ptr.close()

def csv_row_formatter(crse: Course) -> str:
    return f"{surround_quotes(crse.department)},{surround_quotes(crse.course_code)},{surround_quotes(crse.title)},{surround_quotes(crse.credit_info)},{surround_quotes(crse.prereq)},{surround_quotes(crse.description)}\n"

def surround_quotes(in_str: str)-> str:
    """surround input string with quotes"""
    out_str = in_str
    out_str = out_str.replace('"', '\\"')
    out_str = out_str.replace('\n', ' ')
    out_str = out_str.replace('\t', ' ')
    out_str= out_str.replace('\xa0', ' ')
    if out_str == "":
        out_str = "None"
    return f"\"{out_str.strip()}\""

def sanitize_text(in_str: str) -> str:
    """clean the text from werid stuff and replace with spaces"""
    out_str = in_str.replace('\n', ' ')
    out_str = out_str.replace('\t', ' ')
    out_str= out_str.replace('\xa0', ' ')
    return out_str


main()
