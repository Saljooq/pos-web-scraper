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

    url = "https://catalog.iastate.edu/azcourses/hist/"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")


    parser = CustomParse()

    parser.feed(html)

    list_courses = parser.get_course_list()

    print(f"list size {len(list_courses)}\n")

    # writing the headers of the file
    file_ptr.write("course_num,credit_info,requirement,description\n")


    for i, crse in enumerate(list_courses):
        file_ptr.write(csv_row_formatter(crse))


    file_ptr.close()

def csv_row_formatter(crse: Course) -> str:
    return f"{surround_quotes(crse.title)},{surround_quotes(crse.credit_info)},{surround_quotes(crse.prereq)},{surround_quotes(crse.description)}\n"

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



main()
