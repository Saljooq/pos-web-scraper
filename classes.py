#!/usr/bin/python3
from typing import List
from html.parser import HTMLParser

class Course:
    title: str = ""
    department = ""
    course_code: str = ""
    credit_info: str = ""
    description: str = ""
    prereq: str = ""

class CustomParse(HTMLParser):

    curr_couse: Course = None
    start_processing_course: bool = False
    start_processing_title: bool = False
    start_processing_description_block: bool = False
    start_processing_credit_info: bool = False
    start_processing_description_string: bool = False
    start_processing_prereq:bool = False
    list_of_courses: List[Course] = []

    def __init__(self):
        HTMLParser.__init__(self)

    # for starting tag
    def handle_starttag(self, tag, attrs):

        if tag=='div' and ('class','courseblock') in attrs:
            self.curr_couse = Course()
            self.start_processing_course = True

        if tag=='div' and ('class','courseblocktitle') in attrs:
            self.start_processing_title = True

        if tag=='div' and ('class', 'courseblockdesc accordion-content') in attrs:
            self.start_processing_description_block = True

        if self.start_processing_description_block:
            if tag=='p' and ('class', 'credits noindent') in attrs:
                self.start_processing_credit_info = True

            if tag=='br':
                self.start_processing_description_string = True

            if tag=='p' and ('class', 'prereq') in attrs:
                self.start_processing_prereq = True

    # for handle data
    def handle_data(self, data):
        if self.start_processing_title:
            self.curr_couse.title += data
        elif self.start_processing_description_block:
            if self.start_processing_credit_info:
                self.curr_couse.credit_info += data
            # the description string has to be checked first because pre-req div doesn't
            # close until the desc string has been processed even though it opens before
            elif self.start_processing_description_string:
                self.curr_couse.description += data
            elif self.start_processing_prereq:
                self.curr_couse.prereq += data

    # for end tag
    def handle_endtag(self, tag):
        if tag=='div':
            if self.start_processing_title:
                self.start_processing_title = False
            elif self.start_processing_description_block:
                self.start_processing_description_block = False
                self.start_processing_description_string = False
            elif self.start_processing_course:
                self.start_processing_course = False
                self.list_of_courses.append(self.curr_couse)
        if tag=='p':
            if self.start_processing_credit_info:
                self.start_processing_credit_info = False
            if self.start_processing_prereq:
                self.start_processing_prereq = False

    def get_course_list(self):
        return self.list_of_courses
