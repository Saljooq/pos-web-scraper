#!/usr/bin/python3
from typing import List, Tuple
from urllib.request import urlopen
import re
import os
import sys
import html as htmllib
from html.parser import HTMLParser
from classes import Course, CustomParse
from getUrls import get_urls

# Saved in database - epos
# Username : maintainers

# To login and run database run 'psql --dbname=epos --username=maintainers'

OUTPUT_FILE = "classes.csv"

def main():

    if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)

    file_ptr = open(OUTPUT_FILE, "w")
    # writing the headers of the file
    file_ptr.write("dept,course_num,title,num_credits,semesters_offered,requirement,description\n")

    parser = CustomParse()

    for url in get_urls():

        # url = "https://catalog.iastate.edu/azcourses/com_s/"
        print(url)
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode("utf-8")

        parser.flush_course_list()
        parser.feed(html)

        list_courses = parser.get_course_list()

        print(f"list size {len(list_courses)}\n")

        for crse in list_courses:
            # first we separate the title and course_code/dept
            title_temp = crse.title.split(':')
            crse.title = ":".join(title_temp[1:])

            # next we separate course_code/dept
            temp_course_code_and_dept = sanitize_text(title_temp[0]).split()
            crse.course_code = temp_course_code_and_dept.pop(-1)
            crse.department = " ".join(temp_course_code_and_dept)

            # Next we detect credits and semester offerred "Cr. R.  F.S."
            re_finding = credit_re.findall(crse.credit_info)
            if len(re_finding) > 0:
                crse.num_credits = re_finding[0]
            else:
                crse.num_credits = "None"

            crse.semesters_offered = ",".join(get_semester_list(crse.credit_info))

            # remove the 'Prereq:' from the beginning of the text
            crse.prereq = crse.prereq.replace("Prereq:", "")

            file_ptr.write(csv_row_formatter(crse))


    file_ptr.close()

def csv_row_formatter(crse: Course) -> str:
    return f"{surround_quotes(crse.department)},{surround_quotes(crse.course_code)},{surround_quotes(crse.title)},{surround_quotes(crse.num_credits)},{surround_quotes(crse.semesters_offered)},{surround_quotes(crse.prereq)},{surround_quotes(crse.description)}\n"

def surround_quotes(in_str: str)-> str:
    """surround input string with quotes"""
    out_str = in_str
    out_str = out_str.replace('"', '\\"')
    out_str = out_str.replace('\n', ' ')
    out_str = out_str.replace('\t', ' ')
    out_str= out_str.replace('\xa0', ' ')
    if out_str == "" or out_str == None:
        out_str = "None"
    return f"\"{out_str.strip()}\""

def sanitize_text(in_str: str) -> str:
    """clean the text from werid stuff and replace with spaces"""
    out_str = in_str.replace('\n', ' ')
    out_str = out_str.replace('\t', ' ')
    out_str= out_str.replace('\xa0', ' ')
    return out_str

# Below are the Regex patterns for semesters and credits

fall_re = re.compile("F\.*") 
spring_re = re.compile("[^S]S\.*") 
summer_re = re.compile("SS\.*")

credit_re = re.compile("Cr\. ([a-zA-Z0-9\-]*)\.")

def get_semester_list(in_str: str) -> List[str]:
    res = []
    if fall_re.search(in_str) != None:
        res.append('fall')
    if spring_re.search(in_str) != None:
        res.append('spring')
    if summer_re.search(in_str) != None:
        res.append('summer')
    return res

main()
