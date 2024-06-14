# A new scraper for pathways, based on the catalog.rpi.edu website

from bs4 import BeautifulSoup as bs
import json
import unicodedata
import requests

# input: none
# output: All of the pathway links in a list, to be processed.
def link_finder() -> list[str]:
    url = "https://catalog.rpi.edu"
    soup_early = bs(requests.get(url).content, "html.parser")
    nav_bar = soup_early.find(id = "acalog-navigation")
    end_link = ""
    for el in nav_bar.find_all("div"):
        if el.find("a").text == "Programs":
            end_link = el.find("a")['href']
    programs_html = requests.get(url + end_link).content
    soup = bs(programs_html, "html.parser")
    strong_elements = soup.find_all('strong')
    for el in strong_elements:
        if 'Pathway' in el.text:
            target_element = el.parent.find_next_sibling()
            break
    links = []
    base = url + "/"
    for el in target_element.find_all('a'):
        new_link = base + el['href']
        links.append(new_link)
        
    return links


# Scrapes pages that don't have subtitles. See: https://catalog.rpi.edu/preview_program.php?catoid=26&poid=7615&returnto=669 for example
# input: page contents (html)
# output: a dictionary containing the pathway info (albeit less specific than other pathways.)

def special_scrape(page: str) -> dict[str : list[str]]:
    soup = bs(page, "html.parser")
    description = soup.find("div", attrs={"class" : "program_description"})
    block = description.find_parent().find_parent().find_parent()
    title = block.find("h1")
    p_tags = description.find_all("p")
    description_text = ""
    for tag in p_tags:
        description_text += str(tag.text)
    
    description_text = description_text.replace("\n", "")
    prefixes = description.find("ul")
    prefixes_text = ""
    first = True
    for el in prefixes.contents:
        if el.text.strip() == "":
            continue
        if first:
            prefixes_text += el.text.replace("\n", "")
            first = False
            continue
        prefixes_text += ", " + el.text.replace("\n", "")

    result = dict()
    result["text"] = " ".join(((description_text + prefixes_text).replace(u"\xa0", " ")).split())
    return result


# input: a link to a pathway (str)
# output: a dictionary containing the pathway info. See: https://github.com/martig7/HASSPathways/blob/main/frontend/src/data/json/2023-2024/pathways.json
# for formatting json from this dictionary.

def scrape_link(link: str) -> dict[str: list[str]]:
    r = requests.get(link)
    page = r.text
    
    soup = bs(page, "html.parser")
    description = soup.find("div", attrs={"class" : "program_description"})
    block = description.find_parent().find_parent().find_parent()
    title = block.find("h1")
    all = block.find("div", attrs={"class" : "custom_leftpad_20"})
    result = dict()
    if (all == None):
        result = special_scrape(page)
        return result
    for el in all.contents:
        subtitle = str(el.find("h2").text.strip())
        courses = el.find_all("li", attrs={"class" : "acalog-course"})
        minor_list = el.find_all("li", attrs={"class" : None})
        adhoc = el.find_all("li", attrs = {"class" : "acalog-adhoc-list-item acalog-adhoc-after"})
        adhoc += el.find_all("li", attrs ={"class" : "acalog-adhoc acalog-adhoc-after"})
        text = ""
        current = dict()
        p_tags = el.find_all("p")
        text_list = []
        course_ids = []
        course_names = []
        if len(p_tags) != 0:
            for tag in p_tags:
                text_list.append(" ".join((str(tag.text.strip()).replace(u"\xa0", " ").replace(u"\n", " ")).split()))
                links = tag.find("a")
                if links != None:
                    for l in links:
                        course_ids.append(l.text)
                        course_names.append("")
            if "Compatible minor" in el.find("h2").text:
                current["minors"] = text_list
            else:
                current["text"] = text_list
        if len(courses) == 0 and len(adhoc) == 0 and len(minor_list) != 0:
            minors = []
            for minor_el in minor_list:
                minors.append(minor_el.text.strip())
            current["minors"] = minors
        if len(courses) > 0:
            for course_el in courses:
                to_split = str(course_el.find("a").text)
                split = to_split.split("-", 1)
                course_ids.append(split[0].strip())
                course_names.append(split[1].strip())
        if len(adhoc) > 0:
            for adhoc_el in adhoc:
                to_split = str(adhoc_el.text)
                if "-" not in to_split:
                    split = to_split.split()
                    course_id_temp = " ".join(split[0:2])
                    rest_joined = " ".join(split[2:])
                    course_name = rest_joined.split(":")[0].removesuffix("Credit Hours")
                    course_ids.append(course_id_temp)
                    course_names.append(course_name)
                else:
                    split = to_split.split("-", 1)
                    course_ids.append(split[0].strip())
                    course_names.append(split[1].strip())
        
        current["course_ids"] = course_ids
        current["course_names"] = course_names
        result[subtitle] = current
    print(result)
    return result
    



links = link_finder()
for i in links:
    print(i)
    scrape_link(i)



#scrape_link("https://catalog.rpi.edu/preview_program.php?catoid=26&poid=7615&returnto=669")