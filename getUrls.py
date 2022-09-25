from typing import Tuple
from urllib.request import urlopen


def get_urls():
    url = "https://catalog.iastate.edu/azcourses/"
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    stringList = html.split("\n")
    major_list = []

    for line in stringList:
        valid, res = fetch_text_in_between(line, starting_pattern="<a href=\"/azcourses/", ending_pattern="\">")
        if valid and res != '':
            major_list.append(res)

    urls = map(lambda a: url + a, major_list)

    return list(urls)


def fetch_text_in_between(original_string: str, starting_pattern: str, ending_pattern: str, other_req_str:str = None)-> Tuple[bool,str]:
    """This method gets the substring from the original string, between starting pattern and ending pattern. Optionally, you can
    pass a required string that will output valid=False if it is not found"""
    valid = original_string.find(starting_pattern) != -1 and original_string.find(starting_pattern) != -1 and original_string.find(ending_pattern) != -1

    if other_req_str != None:
        valid = valid and original_string.find(other_req_str) != -1 

    if valid:
        res_str = original_string[original_string.find(starting_pattern) + len(starting_pattern): original_string.find(ending_pattern)]
        return (valid, res_str)
    else:
        return(valid, None)

