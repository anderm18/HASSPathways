# A new scraper for pathways, based on the catalog.rpi.edu website

from bs4 import BeautifulSoup as bs
import json
import unicodedata
import requests
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# input: course code (str) in form SUBJ #### (e.g.  CSCI 1100)
# output: course name (str) (e.g. Introduction to Computer Science)
def search_for_name(course_code: str) -> str:
    subj, code = course_code.split(" ")
    link = "https://catalog.rpi.edu/search_advanced.php?cur_cat_oid=26&ecpage=1&cpage=1&ppage=1&pcpage=1&spage=1&tpage=1&search_database=Search&filter%5Bkeyword%5D={}+{}&filter%5Bexact_match%5D=1&filter%5B3%5D=1&filter%5B31%5D=1#".format(subj, code)
    soup = bs(requests.get(link).content, "html.parser")
    tag = soup.find("a", attrs={"aria-expanded" : "false"})
    return tag.text.split("-")[1].strip()


# input: none
# output: All of the pathway links in a list, to be processed. Basically navigates to the programs page and scrapes all of the links to the pathways.
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
'''
Big scraping function: Not my best work, but the catalog is a mess. I have tried to comment all of the workarounds I used to format everything properly, but
I may have missed some. This function scrapes a pathway and returns a dictionary with the pathway information. The dictionary is formatted as follows:

{"title" : "Pathway Title", "description" : "Pathway Description", "subtitle1" : {"text" : ["text1", "text2", ...], "course_ids" : ["course_id1", "course_id2", ...], "course_names" : ["course_name1", "course_name2", ...], "minors" : ["minor1", "minor2", ...]}, "subtitle2" : {"text" : ["text1", "text2", ...], "course_ids" : ["course_id1", "course_id2", ...], "course_names" : ["course_name1", "course_name2", ...], "minors" : ["minor1", "minor2", ...]}, ...
'''

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
        result["description"] = " ".join((str(description.text.strip()).replace(u"\xa0", " ").replace(u"\n", " ").replace(u"\u201c", "")).split()) # this messy formatting is because of encoding issues.

        """
        This part should extract the correct elements from a subtitle for each type of data. Adhoc is are the courses that do not have a link with them
        and are stored in plain text. P_tags should get everything that's just text, which only works because we extract the courses and adhoc elements.
        The minors should be stored in the li tags with no class name, but sometimes they are instead stored in the p tags. This is why we assign
        minors in both the p_tags block and the minors block. I do not know what to make of this pattern-wise except that the catalog sucks.
        """
        subtitle = str(el.find("h2").text.strip())
        courses = el.find_all("li", attrs={"class" : "acalog-course"})
        minor_list = el.find_all("li", attrs={"class" : None})
        adhoc = el.find_all("li", attrs = {"class" : "acalog-adhoc-list-item acalog-adhoc-after"})
        adhoc += el.find_all("li", attrs ={"class" : "acalog-adhoc acalog-adhoc-after"})
        for course in courses:
            course.extract()
        for ad in adhoc:
            ad.extract()
        if ("minor" not in subtitle):
            adhoc += el.find_all("li")
        p_tags = el.find_all("p")

        text = ""
        current = dict()
        text_list = []
        course_ids = []
        course_names = []
        if len(p_tags) != 0:
            for tag in p_tags:
                text_list.append(" ".join((str(tag.text.strip()).replace(u"\xa0", " ").replace(u"\n", " ")).split()))
                links = tag.find("a")
                if (subtitle == "Compatible minor:"): # checks that the link we grabbed was part of a minor subtitle, meaning it's not a course.
                    continue
                # checks for extra courses in the p_tags (these are usually required, so they are important)
                if links != None:
                    for l in links:
                        course_ids.append(l.text)
                        course_names.append(search_for_name(l.text))
            if "Compatible minor" in el.find("h2").text:
                current["minors"] = text_list
            else:
                current["text"] = text_list
        # scrapes minors
        if len(courses) == 0 and len(adhoc) == 0 and len(minor_list) != 0 or "Compatible minors" in subtitle:
            minors = []
            for minor_el in minor_list:
                minor_link = minor_el.find("a")
                if minor_link != None: # this is if the minor has a link
                    minors.append(minor_link.text.strip()) 
                else: # if not just add the text from the whole element. Should only be the Music and Sound pathway.
                    minors.append(minor_el.text.strip())
            current["minors"] = minors

        # this part scrapes courses from the adhoc and course elements, and is a lot more straightforward. 
        # Just be careful that if a course title contains a "-" or ":", it will need to be handled correctly.
        if len(courses) > 0:
            for course_el in courses:
                to_split = str(course_el.find("a").text)
                if "–" in to_split:
                    to_split = to_split.replace("–", "-")
                if "-" not in to_split:
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
        if len(adhoc) > 0:
            for adhoc_el in adhoc:
                small_ps = adhoc_el.find_all("p")
                if len(small_ps) == 0:
                    small_ps = [adhoc_el]
                for tag in small_ps:
                    to_split = str(tag.text)
                    if "-" not in to_split:
                        if (len(to_split) < 9): # checks if to_split is actually a course
                            continue
                        split = to_split.split()
                        course_id_temp = " ".join(split[0:2])
                        if len(course_id_temp) != 9:
                            continue
                        rest_joined = " ".join(split[2:])
                        course_name = rest_joined.rsplit(":", 1)[0].removesuffix("Credit Hours") # rsplit splits from the right, so it's sort of like .split(":" , -1) if that was a thing that existed
                        course_ids.append(course_id_temp.strip())
                        course_names.append(course_name.strip())
                    else:
                        split = to_split.split("-", 1)
                        if len(split[0].strip()) != 9:
                            continue
                        course_ids.append(split[0].strip())
                        course_name = split[1].strip()
                        if ("Credit Hours" in split[1]):
                            course_name = split[1].strip().rsplit(":", 1)[0].removesuffix("Credit Hours")
                        elif ("Credit Hours" not in split[1]):
                            course_name = split[1].strip().split("(", 1)[0].strip()
                        course_names.append(course_name.strip())
        
        current["course_ids"] = course_ids
        current["course_names"] = course_names  
        result[subtitle] = current
    return result


'''
A QUICK GUIDE TO SUBTITLE CLASSIFICATION: This is stored in subtitle_classification.json, and is the only thing that needs to be manually updated on
a per-year basis. This is because each pathway is inconsistent in its formatting, so we must tell the scraper how to interpret each pathway's subtitles.
This json is formatted with the type of subtitle as the key, and the value as a list of the subtitles that fall under that category.
They are defined as follows:

- Required: These are courses that are required for the pathway. They may be listed individually or as a group. Something is required if the courses are
listed with an "AND". (e.g. "CSCI 1100 AND CSCI 1200" would be required). If the courses are listed with an "OR", they are classified as "One Of0", "One Of1", etc.

- oneOf0, oneOf1, oneOf2: These are courses that are required, but only one of them is needed. We only go up to oneOf2 because pathways only require 12 credits, so
3 oneOfs would satisfy the 12 credit requirement.

- Remaining: These are courses that students may take to satisfy the remaining of their 12 credit requirement. If a subtitle doesn't fit into the other categories
and it lists courses, then it is probably remaining (with the exception of courses labelled "optional"). 

- remaining_header: This is the subtitle which holds the details of what exactly "Remaining" means for the course. This may or may not be the same subtitle as remaining.

- minor: This is the subtitle that holds the minors that are compatible with the pathway. Should usually be "Compatible minor:" or "Compatible minors".


json_builder: This function takes in a dictionary of pathways and outputs a json that is formatted to be used in the frontend. It uses the subtitle_classification.json file
to distinguish the subtiles within the pathways. If this stops working, it's likely because of a KeyError which means that the subtitle_classification.json file is not up to date.

'''

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

# Test for one pathway. Should print a json to console.

def test_one(link):
    pathways = dict()
    temp = scrape_link(link)
    pathways[temp["title"]] = temp
    final = json_builder(pathways)
    out = json.dumps(final, indent= 4)
    print(out)
    return

# Main functiom which scrapes all pathways and outputs to a json file to the file location.

def scrape_all(location):
    print("Finding Links...")
    links = link_finder()
    pathways = dict()
    print("Scraping Pathways...")
    for i in links:
        temp = scrape_link(i)
        print("Pathway Scraped: " + temp["title"])
        pathways[temp["title"]] = temp

    print("Building JSON...")
    final = json_builder(pathways)
    out = json.dumps(final, indent= 4)
    with open(location, 'w') as f:
        f.write(out)
    return
    
'''
VERIFICATION: This function will parse two jsons as dictionaries and compare them. It will output this to verify_file_loc.

KEEP IN MIND: To check if something goes wrong, you will have to read through this verification file. 
The most important thing to look out for is Missing keys, because this means that the new pathways file is missing information that the old one had.
Check that this is accurate by going to the rpi catalog.

This checks each pathway in the order that the json is formatted, which should also be the order they are listed on the website.

Sometimes if a key is missing it is because it was replaced with a different key, but it still has the same data. For instance,
a oneOf may be replaced with a required, but the data is the same. This is not an issue.

'''

def verify_output(json_new, json_old, verify_file_loc):
    new = dict()
    old = dict()
    with open(json_new, 'r') as f:
        new = json.load(f)
    with open(json_old, 'r') as f:
        old = json.load(f)
    verify = ""
    for i in new.keys():
        
        verify += "----------------------------------------------------------------------------------------------------\n"
        
        if i not in old.keys():
            verify += "New Pathway: " + i + "\n"
            continue
        elif new[i] != old[i]:
            verify += "Pathway name: " + i + "\n"
            for j in new[i].keys():
                if j not in old[i].keys():
                    verify += "New key in " + i + ": " + j + "\n"
                elif new[i][j] != old[i][j]:
                    verify += "Difference in " + i + " in " + j + "\n"
                    if type(new[i][j]) == dict:
                        for k in new[i][j].keys():
                            if k not in old[i][j].keys():
                                verify += "New key in " + j + ": " + k + "\n"
                            elif new[i][j][k] != old[i][j][k]:
                                verify += "Difference in " + i + " in " + j + " in " + k + "\n"
                                verify += "Old: " + str(old[i][j][k]) + "\n"
                                verify += "New: " + str(new[i][j][k]) + "\n"
                        for k in old[i][j].keys():
                            if k not in new[i][j].keys():
                                verify += "Missing key in " + j + ": " + k + "\n"
                        
                    else:
                        verify += "Old: " + str(old[i][j]) + "\n"
                        verify += "New: " + str(new[i][j]) + "\n"
            for j in old[i].keys():
                if j not in new[i].keys():
                    verify += "Missing key in " + i + ": " + j + "\n"
        else:
            verify += "Pathway name: " + i + "\n"

        with open(verify_file_loc, 'w') as f:
            f.write(verify)
    
if __name__ == "__main__":
    year = "2024-2025"
    parent_path = os.path.dirname(os.path.dirname(dir_path))
    json_path = os.path.join(parent_path, "frontend", "src", "data", "json")
    path = os.path.join(json_path, str(year))
    pathway_loc = os.path.join(path, 'pathways.json')
    old_pathway_loc = os.path.join(path, 'pathways_old.json')
    verify_loc = os.path.join(path, 'verify.txt')
    scrape_all(pathway_loc)
    print("Verifying...")
    verify_output(pathway_loc, old_pathway_loc, verify_loc)



