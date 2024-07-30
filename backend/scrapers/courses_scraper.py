from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import *
import os
import json
import time
import re
from itertools import chain
import ci_scraper as ci

def un_spaceify(string: str) -> str:
    string = re.sub("\xa0", " ", string)
    string = re.sub(" +", " ", string)
    string = re.sub(r"\s(?=[,.;!/]|$)", "", string)
    string = re.sub(r"^ (?=\w)", "", string)
    return string

def re_spaceify(string: str) -> str:
    string = re.sub(r".(?=\w)", ". ", string)
    

def scrape_single_course(driver: Firefox, prefix:str, code:str, cis: list[str]) -> dict:
    link = "https://catalog.rpi.edu/content.php?filter%5B27%5D={}&filter%5B29%5D={}&filter%5Bkeyword%5D=&filter%5B32%5D=1&filter%5Bcpage%5D=1&cur_cat_oid=30&expand=&navoid=788&search_database=Filter&filter%5Bexact_match%5D=1#acalog_template_course_filter".format(prefix, code)
    driver.get(link)
    wait = WebDriverWait(driver, timeout=1, ignored_exceptions=(NoSuchElementException))
    try:
        wait.until(lambda d : driver.find_element(By.CSS_SELECTOR, ".width > a:nth-child(1)").is_displayed())
    except TimeoutException:
        if 'X' in code:
            return scrape_single_course(driver, prefix, code.replace('X', '0'), cis)
        else:
            if int(code[3]) < 9:
                return scrape_single_course(driver, prefix, str(int(code) + 1), cis)
            return dict()
    driver.find_element(By.CSS_SELECTOR, ".width > a:nth-child(1)").click()
    second_wait = WebDriverWait(driver, timeout=10, ignored_exceptions=(NoSuchElementException))
    try:
        second_wait.until(lambda d : driver.find_element(By.XPATH, "/html/body/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/div[2]").is_displayed())
    except TimeoutException:
        print("Something probably went wrong with the XPATH")
    ele = driver.find_element(By.XPATH, "/html/body/table/tbody/tr[3]/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table[2]/tbody/tr[2]/td[2]/table/tbody/tr/td/div[2]")
    content = ele.get_attribute('innerHTML')
    soup = bs(content, "html.parser")
    title = soup.find("h3")
    title.extract()
    closes = soup.find_all("div")
    for close in closes:
        close.extract()
    a_tags = soup.find_all("a")
    classes_mentioned = []
    for a in a_tags:
        temp = a.get_text(strip=True)
        classes_mentioned.append(temp)
    s_string = str(soup)
    parts = s_string.split("<strong>")
    description_html = parts[0]
    desc_soup = bs(description_html, "html.parser")
    description = un_spaceify(desc_soup.get_text())
    rest = s_string.removeprefix(description_html)
    r_soup = bs(rest, "html.parser")
    rest_text = r_soup.get_text()
    delimiters = ["Prerequisites/Corequisites:","Cross Listed:", "When Offered:", "Credit Hours:", "Co-Listed:", "Contact, Lecture or Lab Hours:", "Graded:"]
    built_list = [rest_text]
    for de in delimiters:
        t = []
        for l in built_list:
            splitted = l.split(de, 1)
            if de in l:
                splitted[1] = de + splitted[1]
            t.append(splitted)
                
        built_list = list(chain.from_iterable(t))
    if len(built_list) != 0:
        built_list.pop(0)
    
    for i in range(len(built_list)):
        built_list[i] = un_spaceify(built_list[i])
    result = dict()
    title = title.get_text(strip=True)
    result = dict()
    result["prerequisites"] = prerequisite_constructor(built_list, classes_mentioned)
    result["cross listed"] = crosslisted_constructor(built_list, classes_mentioned)
    result["description"] = description
    result["name"] = un_spaceify(title.split("-")[1])
    result["offered"] = when_offered_constructor(built_list)
    result["properties"] = properties_constructor(prefix, code, cis)
    result["subj"] = prefix
    result["ID"] = code
    return result

def properties_constructor(prefix: str, code: str, cis: list[str]):
    result = dict()
    result["HI"] = (prefix == "INQR")
    result["CI"] = (prefix + "-" + code in cis)
    result["major_restricted"] = False # no good way to check this right now, should never be true because it's a pathway
    return result
    
def prerequisite_constructor(course_data: list[str], courses_mentioned: list[str]):
    prereq_list = []
    looking = ""
    for i in course_data:
        if "Prerequisites/Corequisites:" in i:
            looking = i
    
    for course in courses_mentioned:
        if course in looking:
            prereq_list.append(course)
    return prereq_list
    
def crosslisted_constructor(course_data: list[str], courses_mentioned: list[str]):
    crosslist_list = set()
    looking_cross = ""
    looking_co = ""
    for i in course_data:
        if "Cross Listed:" in i:
            looking_cross = i
        if "Co-Listed:" in i:
            looking_co = i
    for course in courses_mentioned:
        if course in looking_cross:
            crosslist_list.add(course)
        if course in looking_co:
            crosslist_list.add(course)
    return list(crosslist_list)


def when_offered_constructor(course_data: list[str]):
    result = dict()
    result["even"] = False
    result["odd"] = False
    result["fall"] = False
    result["spring"] = False
    result["summer"] = False
    result["uia"] = False
    result["text"] = ""
    for i in course_data:
        if "when offered:" in i.lower():
            result["text"] = i
    if "even years" in result["text"].lower() or "even-numbered" in result["text"].lower():
        result["even"] = True
    if "odd years" in result["text"].lower() or "odd-numbered" in result["text"].lower():
        result["odd"] = True
    if "fall" in result["text"].lower():
        result["fall"] = True
    if "spring" in result["text"].lower():
        result["spring"] = True
    if "summer" in result["text"].lower():
        result["summer"] = True
    if "availability of instructor" in result["text"].lower() or "upon availability" in result["text"].lower(): 
        result["uia"] = True
    return result




def check_to_scrape(year: int) -> list[str]:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = os.path.dirname(os.path.dirname(dir_path))
    jsons_path = os.path.join(parent_path, "frontend", "src", "data", "json")
    folder_title = "{}-{}".format(year - 1, year)
    json_checking_path = os.path.join(jsons_path, folder_title, "pathways.json")
    to_check = list()
    with open(json_checking_path, 'r') as f:
        j = dict(json.load(f))
    for pathway in j.keys():
        if "Remaining" in j[pathway].keys():
            [to_check.append(i) for i in j[pathway]["Remaining"].values()]
        if "Required" in j[pathway].keys():
            [to_check.append(i) for i in j[pathway]["Required"].values()]
        if "One Of0" in j[pathway].keys():
            [to_check.append(i) for i in j[pathway]["One Of0"].values()]
        if "One Of1" in j[pathway].keys():
            [to_check.append(i) for i in j[pathway]["One Of1"].values()]
        if "One Of2" in j[pathway].keys():
            [to_check.append(i) for i in j[pathway]["One Of2"].values()]
    to_check = list(set(to_check))
    return to_check

def scrape_courses(year: int, pdf_name: str, json_path: str):
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)
    to_check = check_to_scrape(year)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pdf_path = os.path.join(dir_path, 'pdfs', pdf_name)
    cis = ci.parse_pdf(pdf_path)
    all_courses = []
    for course in to_check:
        prefix, code = course.split(" ")
        course_data = scrape_single_course(driver, prefix, code, cis)
        all_courses.append(course_data)

    out = json.dumps(all_courses, indent= 4)
    print(out)
    with open(json_path, 'w') as f:
        f.write(out)
    driver.quit()

scrape_courses(2025)
#driver = webdriver.Firefox()
#driver.implicitly_wait(2)
#scrape_single_course(driver, "ARTS", "4040")
