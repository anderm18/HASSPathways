# A new scraper for pathways, based on the catalog.rpi.edu website

from bs4 import BeautifulSoup as bs
import json
import unicodedata
import requests
import os

mapping = {"Requirements" : "remaining_header"}

# input: course code (str) in form SUBJ #### (e.g.  CSCI 1100)
# output: course name (str) (e.g. Introduction to Computer Science)
def search_for_name(course_code: str) -> str:
    subj, code = course_code.split(" ")
    link = "https://catalog.rpi.edu/search_advanced.php?cur_cat_oid=26&ecpage=1&cpage=1&ppage=1&pcpage=1&spage=1&tpage=1&search_database=Search&filter%5Bkeyword%5D={}+{}&filter%5Bexact_match%5D=1&filter%5B3%5D=1&filter%5B31%5D=1#".format(subj, code)
    soup = bs(requests.get(link).content, "html.parser")
    tag = soup.find("a", attrs={"aria-expanded" : "false"})
    return tag.text.split("-")[1].strip()


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
        result["title"] = title.text
        result["description"] = " ".join((str(description.text.strip()).replace(u"\xa0", " ").replace(u"\n", " ")).split())
        return result
    for el in all.contents:
        result["title"] = title.text
        result["description"] = " ".join((str(description.text.strip()).replace(u"\xa0", " ").replace(u"\n", " ").replace(u"\u201c", "")).split())
        subtitle = str(el.find("h2").text.strip())
        courses = el.find_all("li", attrs={"class" : "acalog-course"})
        minor_list = el.find_all("li", attrs={"class" : None})
        adhoc = el.find_all("li", attrs = {"class" : "acalog-adhoc-list-item acalog-adhoc-after"})
        adhoc += el.find_all("li", attrs ={"class" : "acalog-adhoc acalog-adhoc-after"})
        for ad in adhoc:
            ad.extract()
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
                if (subtitle == "Compatible minor:"):
                    continue
                if links != None:
                    for l in links:
                        course_ids.append(l.text)
                        course_names.append(search_for_name(l.text))
            if "Compatible minor" in el.find("h2").text:
                current["minors"] = text_list
            else:
                current["text"] = text_list
        if len(courses) == 0 and len(adhoc) == 0 and len(minor_list) != 0 or "Compatible minors" in subtitle:
            minors = []
            for minor_el in minor_list:
                minor_link = minor_el.find("a")
                if minor_link != None:
                    minors.append(minor_link.text.strip())
                else:
                    minors.append(minor_el.text.strip())
            current["minors"] = minors
        if len(courses) > 0:
            for course_el in courses:
                to_split = str(course_el.find("a").text)
                if "-" not in to_split:
                    split = to_split.split()
                    course_id_temp = " ".join(split[0:2])
                    rest_joined = " ".join(split[2:])
                    course_name = rest_joined.split(":")[0].removesuffix("Credit Hours")
                    course_ids.append(course_id_temp.strip())
                    course_names.append(course_names.strip())
                else:
                    split = to_split.split("-", 1)
                    course_ids.append(split[0].strip())
                    course_names.append(split[1].strip())
        if len(adhoc) > 0:
            for adhoc_el in adhoc:
                to_split = str(adhoc_el.text)
                if "-" not in to_split:
                    if (len(to_split) < 9):
                        continue
                    split = to_split.split()
                    course_id_temp = " ".join(split[0:2])
                    rest_joined = " ".join(split[2:])
                    course_name = rest_joined.split(":")[0].removesuffix("Credit Hours")
                    course_ids.append(course_id_temp.strip())
                    course_names.append(course_name.strip())
                else:
                    split = to_split.split("-", 1)
                    course_ids.append(split[0].strip())
                    course_names.append(split[1].strip())
        
        current["course_ids"] = course_ids
        current["course_names"] = course_names  
        result[subtitle] = current
    return result
    

def json_builder(pathways) -> dict[str: dict]:
    final = dict()
    classifications = dict()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, "subtitle_classification.json"), 'r') as f:
        classifications = json.load(f)
    for i in classifications.keys():
        pathway_name = i + " Pathway"
        if pathway_name not in pathways.keys():
            continue
        
        final[i] = dict()
        final[i]["name"] = i
        final[i]["description"] = pathways[pathway_name]["description"]
        if "remaining_header" in classifications[i].keys():
            for j in classifications[i]["remaining_header"]:
                if "text" in pathways[pathway_name][j].keys():
                    final[i]["remaining_header"] = " ".join(pathways[pathway_name][j]["text"])
        if "Remaining" in classifications[i].keys():
            final[i]["Remaining"] = dict()
            for j in classifications[i]["Remaining"]:
                if "course_ids" in pathways[pathway_name][j].keys() and "course_names" in pathways[pathway_name][j].keys():
                    course_names = pathways[pathway_name][j]["course_names"]
                    course_ids = pathways[pathway_name][j]["course_ids"]
                    for x in range(len(course_names)):
                        final[i]["Remaining"][course_names[x]] = course_ids[x]
        if "minor" in classifications[i].keys():
            final[i]["minor"] = []
            
            for j in classifications[i]["minor"]:
                final[i]["minor"] += pathways[pathway_name][j]["minors"]
        
        if "Required" in classifications[i].keys():
            final[i]["Required"] = dict()
            for j in classifications[i]["Required"]:
                if "course_ids" in pathways[pathway_name][j].keys() and "course_names" in pathways[pathway_name][j].keys():
                    course_names = pathways[pathway_name][j]["course_names"]
                    course_ids = pathways[pathway_name][j]["course_ids"]
                    for x in range(len(course_names)):
                        if course_names[x] not in final[i]["Required"]:
                            final[i]["Required"][course_names[x]] = course_ids[x]
                    
    
        if "One Of0" in classifications[i].keys():
            final[i]["One Of0"] = dict()
            for j in classifications[i]["One Of0"]:
                if "course_ids" in pathways[pathway_name][j].keys() and "course_names" in pathways[pathway_name][j].keys():
                    course_names = pathways[pathway_name][j]["course_names"]
                    course_ids = pathways[pathway_name][j]["course_ids"]
                    for x in range(len(course_names)):
                        final[i]["One Of0"][course_names[x]] = course_ids[x]

        if "One Of1" in classifications[i].keys():
            final[i]["One Of1"] = dict()
            for j in classifications[i]["One Of1"]:
                if "course_ids" in pathways[pathway_name][j].keys() and "course_names" in pathways[pathway_name][j].keys():
                    course_names = pathways[pathway_name][j]["course_names"]
                    course_ids = pathways[pathway_name][j]["course_ids"]
                    for x in range(len(course_names)):
                        final[i]["One Of1"][course_names[x]] = course_ids[x]
        
        if "One Of2" in classifications[i].keys():
            final[i]["One Of2"] = dict()
            for j in classifications[i]["One Of2"]:
                if "course_ids" in pathways[pathway_name][j].keys() and "course_names" in pathways[pathway_name][j].keys():
                    course_names = pathways[pathway_name][j]["course_names"]
                    course_ids = pathways[pathway_name][j]["course_ids"]
                    for x in range(len(course_names)):
                        final[i]["One Of2"][course_names[x]] = course_ids[x]

    
    return final


def test_one(link):
    pathways = dict()
    temp = scrape_link(link)
    pathways[temp["title"]] = temp
    final = json_builder(pathways)
    out = json.dumps(final, indent= 4)
    print(out)
    return

def scrape_all(location):
    links = link_finder()
    pathways = dict()
    for i in links:
        temp = scrape_link(i)
        pathways[temp["title"]] = temp

    final = json_builder(pathways)
    out = json.dumps(final, indent= 4)
    with open(location, 'w') as f:
        f.write(out)
    return
    
    
if "__name__" == "__main__":
    scrape_all()



scrape_all("pathways_new.json")
#print(search_for_name("CSCI 1100"))