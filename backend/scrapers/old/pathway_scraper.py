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
CHUNK_SIZE = 500

# returns the list of catalogs with the newest one being first
# each catalog is a tuple (year, catalog_id) ex: ('2020-2021', 21)
def get_catalogs() -> List[Tuple[str, int]]:
    catalogs_xml = html.fromstring(
        requests.get(
            f"{BASE_URL}content{DEFAULT_QUERY_PARAMS}&method=getCatalogs"
        ).text.encode("utf8")
    )
    catalogs = catalogs_xml.xpath("//catalogs/catalog")
    print(f"{BASE_URL}content{DEFAULT_QUERY_PARAMS}&method=getCatalogs")
    print(len(catalogs))
    ret: List[Tuple[str, int]] = []
    # For each catalog get its year and id and add that as as tuples to ret
    for catalog in catalogs:
        catalog_id: int = catalog.xpath("@id")[0].split("acalog-catalog-")[1]
        catalog_year: str = [
            text for text in catalog.xpath(".//text()") if "Rensselaer Catalog " in text
        ][0].split("Rensselaer Catalog ")[1]
        print(catalog_year)
        ret.append((catalog_year, catalog_id))

    # sort so that the newest catalog is always first
    ret.sort(key=lambda tup: tup[0], reverse=True)
    return ret


# Returns a list of course ids for a given catalog
def get_pathway_ids(catalog_id: str) -> List[str]:
    programs_xml = etree.fromstring(
        requests.get(
            f"{BASE_URL}search/programs{DEFAULT_QUERY_PARAMS}&method=listing&options[limit]=0&catalog={catalog_id}"
        ).text.encode("utf8")
    )
    return programs_xml.xpath('//result[type="Integrative Pathway"]/id/text()')

def course_from_string(inp, depts):
    for dept in depts:
        fnd = inp.find(dept)
        if fnd != -1:
            if inp[fnd+8].isdigit() or inp[fnd+8] == "X":
                if inp[fnd+5] != '6':
                    return inp[fnd:fnd+4] + inp[fnd+5:fnd+9]

def handle_electives(cont, courses, depts, year):
    level = '0'
    for char in cont:
        if char.isdigit():
            level = char
            break
    if level == '0':
        return
    subj = "TEMP"
    for word in cont.split():
        if word in depts:
            subj = word
            break
    if subj == "TEMP":
        return
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = os.path.dirname(os.path.dirname(dir_path))
    json_path = os.path.join(parent_path, "frontend", "src", "data", "json")
    path = os.path.join(json_path, str(year))
    f = open(path + 'courses.json', 'r')
    all_courses = json.load(f)
    for course in all_courses:
        ID = all_courses[course]["ID"]
        subjC = all_courses[course]["subj"]
        if ID[0] == level and subjC == subj:
            courses[course.encode("ascii", "ignore").strip().decode().strip()] = subjC+ID
    f.close()

def parse_courses(core, name, year):
    courses = {}
    depts = []
    f = open('depts.json', 'r')
    f = json.load(f)
    for dept in f:
        depts.append(dept)

    tmp = core.xpath("./content/ul/li/descendant-or-self::*/text()")
    tmp += core.xpath("./courses/adhoc/content/ul/li/descendant-or-self::*/text()")
    content = []

    for t in tmp:
        app = False
        for s in t.split():
            if s in depts:
                app = True
        if app:
            t = (t.strip())
            t = t.encode("ascii", "ignore").strip().decode().strip()
            content.append(t)
    if not(len(content) == 0):
        for cont in content:
            if "transfer" in name.lower():
                crs = cont + "XXXX"
                courses[crs] = crs
            # handle as an elective meaning we will have to some funky stuff
            elif "elective" in cont.lower() or "any" in cont.lower() or "level" in cont.lower():
                handle_electives(cont, courses, depts, year)
            else:
                subjID = course_from_string(cont, depts)
                name = ""
                if "-" in cont:
                    name = cont.split("-", 1)[1].strip()
                else:
                    name = cont.split(subjID[4:])[1].strip()
                courses[name] = subjID
    courses_xml = core.xpath("./courses/include/fallback/title/text()")

    for course in courses_xml:
        # fixes all weird unicode and stuff
        course = course.strip().encode("ascii", "ignore").strip().decode()
        subjID = course_from_string(course, depts)
        name = course.split("-", 1)[1].split("Credit")[0].strip()
        courses[name] = subjID
    return courses

def get_pathway_data(pathway_ids: List[str], catalog_id, year) -> Dict:
    data = {}

    ids = "".join([f"&ids[]={path}" for path in pathway_ids])
    url = f"{BASE_URL}content{DEFAULT_QUERY_PARAMS}&method=getItems&options[full]=1&catalog={catalog_id}&type=programs{ids}"

    pathways_xml = html.fromstring(requests.get(url).text.encode("utf8"))

    pathways = pathways_xml.xpath("//programs/program[not(@child-of)]");
    for pathway in pathways:
        name = pathway.xpath("./title/text()")[0].strip()
        data[name] = {}
        data[name]["name"] = name
        desc = ""
        if len(pathway.xpath("./content/p/text()")) >= 1:
            desc = pathway.xpath("./content/p/text()")[0].strip()
        data[name]["description"] = desc.encode("ascii", "ignore").strip().decode()
        cores = pathway.xpath("./cores/core")
        cores += pathway.xpath("./cores/core/children/core")
        one_of_index = 0

        for core in cores:
            anchor_name = core.xpath("./anchors/a")[0].get('name').lower()

            if "required" in anchor_name:
                courses = parse_courses(core, name, year)
                data[name]["Required"] = courses
            elif "oneof" in anchor_name:
                courses = parse_courses(core, name, year)
                one_of_name = "One Of" + str(one_of_index)
                data[name][one_of_name] = courses
                one_of_index += 1
            elif "minor" in anchor_name:
                minors = list(filter(lambda x: x != "", \
                 [minor.replace("Minor", "").replace("minor", "").encode("ascii", "ignore").strip().decode() \
                 for minor in core.xpath("./content/descendant::*/text()")]))
                data[name]["minor"] = minors
            else:
                courses = parse_courses(core, name, year)
                data[name]["Remaining"] = courses
                data[name]["remaining_header"] = core.xpath("./title/text()")[0].strip().encode("ascii", "ignore").strip().decode()

        # get rid of duplicates (if it shows up in required, we don't want it to be optional too)
        if "Required" in data[name]:
            for req in data[name]["Required"]:
                for type in data[name]:
                    if (type == "Remaining" or type[0:6] == "One Of") and req in data[name][type]:
                        del data[name][type][req]
    return data

def scrape_pathways():
    print("Starting pathway scraping")
    catalogs = get_catalogs()

    catalogs = catalogs[:4]
    pathways_per_year = {}
    for index, (year, catalog_id) in enumerate(tqdm(catalogs)):
        pathway_ids = get_pathway_ids(catalog_id)
        data = get_pathway_data(pathway_ids, catalog_id, year)

        pathways_per_year[year] = data
    print("Finished pathway scraping")
    return pathways_per_year
