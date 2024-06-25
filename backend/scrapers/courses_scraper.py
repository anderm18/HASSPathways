# This scraper is mainly sourced from the QUACs team and
# is a modified version of their catalog scraper

from typing import Dict, List, Tuple
import requests
import sys
from lxml import html
import os
from tqdm import tqdm
import json
from lxml import etree
import csv

# The api key is public so it does not need to be hidden in a .env file
BASE_URL = "http://rpi.apis.acalog.com/v1/"
# It is ok to publish this key because I found it online already public
DEFAULT_QUERY_PARAMS = "?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml"
CHUNK_SIZE = 100


# returns the list of catalogs with the newest one being first
# each catalog is a tuple (year, catalog_id) ex: ('2020-2021', 21)
def get_catalogs() -> List[Tuple[str, int]]:
    catalogs_xml = html.fromstring(
        requests.get(
            f"{BASE_URL}content{DEFAULT_QUERY_PARAMS}&method=getCatalogs"
        ).text.encode("utf8")
    )
    catalogs = catalogs_xml.xpath("//catalogs/catalog")

    ret: List[Tuple[str, int]] = []
    # For each catalog get its year and id and add that as as tuples to ret
    for catalog in catalogs:
        catalog_id: int = catalog.xpath("@id")[0].split("acalog-catalog-")[1]
        catalog_year: str = [
            text for text in catalog.xpath("//text()") if "Rensselaer Catalog " in text
        ][0].split("Rensselaer Catalog ")[1]
        ret.append((catalog_year, catalog_id))

    # sort so that the newest catalog is always first
    ret.sort(key=lambda tup: tup[0], reverse=True)
    return ret


# Returns a list of course ids for a given catalog
def get_course_ids(catalog_id: str) -> List[str]:
    courses_xml = html.fromstring(
        requests.get(
            f"{BASE_URL}search/courses{DEFAULT_QUERY_PARAMS}&method=listing&options[limit]=0&catalog={catalog_id}"
        ).text.encode("utf8")
    )
    return courses_xml.xpath("//id/text()")


# Finds and returns a cleaned up description of the course
def get_catalog_description(fields, course_name):
    found_name = False
    # The description is always the next full field after the course name field
    # Itearte through the fields until we find the course name field and then return the next filled field
    for field in fields:
        if found_name == False:
            name = field.xpath(".//*/text()")
            if name and name[0] == course_name:
                found_name = True
        else:
            description = field.xpath(".//*/text()")
            if description:
                clean_description = " ".join(" ".join(description).split())
                # Short descriptions are usually false positives
                if clean_description.startswith("Prerequisite"):
                    return ""
                elif len(clean_description) > 10:
                    return clean_description.encode("ascii", "ignore").strip().decode().strip()

    return ""

def courses_from_string(inp):
    depts = []

    f = open('depts.json', 'r')
    f = json.load(f)

    for dept in f:
        depts.append(dept)

    crses = set()
    for dept in depts:
        fnd = inp.find(dept)
        while fnd != -1:
            if fnd+8 < len(inp):
                if inp[fnd+8].isdigit():
                    if inp[fnd+5] != '6':
                        crses.add(inp[fnd:fnd+4] + '-' + inp[fnd+5:fnd+9])
            fnd = inp.find(dept, fnd + 9)
    return list(crses)

def get_course_data(course_ids: List[str], catalog_id) -> Dict:
    data = {}
    # Break the courses into chunks of CHUNK_SIZE to make the api happy
    course_chunks = [
        course_ids[i : i + CHUNK_SIZE] for i in range(0, len(course_ids), CHUNK_SIZE)
    ]

    depts = []
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + '\\depts.json', 'r')
    f = json.load(f)

    for dept in f:
        depts.append(dept)

    for chunk in course_chunks:
        ids = "".join([f"&ids[]={id}" for id in chunk])
        url = f"{BASE_URL}content{DEFAULT_QUERY_PARAMS}&method=getItems&options[full]=1&catalog={catalog_id}&type=courses{ids}"

        courses_xml = html.fromstring(requests.get(url).text.encode("utf8"))
        courses = courses_xml.xpath("//courses/course[not(@child-of)]")
        for course in courses:
            subj = course.xpath("./content/prefix/text()")[0].strip()
            if not (subj in depts):
                continue
            ID = course.xpath("./content/code/text()")[0].strip()
            if ID[0] == '6':
                continue
            course_name = course.xpath("./content/name/text()")[0].strip()
            fields = course.xpath("./content/field")
            fall = False
            UIA = False
            spring = False
            summer = False
            even = False
            odd = False
            offered_text = ""
            cross_listed = []
            prereqs = []

            base = int(fields[0].get('type')[-3:])
            for field in fields:
                field_text = field.xpath("./descendant-or-self::*/text()")
                if len(field_text) > 0:
                    field_text = field_text[0].strip()

                    if field.get('type')[-3:] == str(base - 8):
                        if len(field_text) > 0:
                            cross_listed = courses_from_string(field_text.upper())
                    elif field.get('type')[-3:] == str(base - 11):
                        if "fall" in field_text.lower():
                            fall = True
                        if "spring" in field_text.lower():
                            spring = True
                        if "summer" in field_text.lower():
                            summer = True
                        if "even" in field_text.lower():
                            even = True
                        if "odd" in field_text.lower():
                            odd = True
                        if "availability of instructor" in field_text.lower():
                            UIA = True
                        offered_text = field_text
                    elif field.get('type')[-3:] == str(base - 13):
                        if len(field_text) > 0:
                            if int(catalog_id) > 23 and field_text.upper().find("PREREQUISITE") != -1:
                                prereqs_list = field.xpath("./descendant-or-self::permalink/title/text()")
                                prereqs = courses_from_string(" ".join(prereqs_list))
                            else:
                                prereqs = courses_from_string(field_text.upper())

            data[course_name] = {
                "subj": subj,
                "ID": ID,
                "name": course_name,
                "description": get_catalog_description(fields, course_name),
                "offered": {
                    "fall": fall,
                    "spring": spring,
                    "summer": summer,
                    "odd": odd,
                    "uia": UIA,
                    "even": even,
                    "text": offered_text
                },
                "properties": {
                    "CI": False,
                    "HI": True if subj == "IHSS" else False,
                    "major_restricted": False
                },
                "cross listed": cross_listed,
                "prerequisites": prereqs
            }

    return data

def scrape_courses():
    print("Starting courses scraping")
    catalogs = get_catalogs()

    catalogs = catalogs[:4]
    courses_per_year = {}
    for index, (year, catalog_id) in enumerate(tqdm(catalogs)):
        course_ids = get_course_ids(catalog_id)
        data = get_course_data(course_ids, catalog_id)
        
        courses_per_year[year] = data

    print("Finished courses scraping")
    return courses_per_year
