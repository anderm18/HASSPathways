import json
import aiohttp
import re
import asyncio
import os
from bs4 import BeautifulSoup
from tqdm import tqdm


import json
import aiohttp
import re
import asyncio
from bs4 import BeautifulSoup
from tqdm import tqdm

async def get_details(ID, subj, curr_year, session):
    years = []
    for i in range(-2, 1):
        new_year = str(int(curr_year[0:4])+i) + str(int(curr_year[-4:])+i)
        years.append(new_year)

    dets = [False, '', dict(), set()]

    for year in years:
        fall = str(year[0:4]) + '09'
        spring = str(year[-4:]) + '01'
        summer = str(year[-4:]) + '05'
        full_soup = None

        async with session.post(
                "https://sis.rpi.edu/rss/bwckctlg.p_disp_listcrse",
                data = f"term_in={fall}&subj_in={subj}&crse_in={ID}&schd_in=L"
        ) as request:
            html = await request.text()

        soup = BeautifulSoup(html, 'html.parser')
        if soup.find(text=re.compile("No classes were found")) == None:
            fall = True
            full_soup = soup
        else:
            fall = False

        async with session.post(
                "https://sis.rpi.edu/rss/bwckctlg.p_disp_listcrse",
                data = f"term_in={spring}&subj_in={subj}&crse_in={ID}&schd_in=L"
        ) as request:
            html = await request.text()

        soup = BeautifulSoup(html, 'html.parser')
        if soup.find(text=re.compile("No classes were found")) == None:
            spring = True
            full_soup = soup
        else:
            spring = False

        async with session.post(
                "https://sis.rpi.edu/rss/bwckctlg.p_disp_listcrse",
                data = f"term_in={summer}&subj_in={subj}&crse_in={ID}&schd_in=L"
        ) as request:
            html = await request.text()

        soup = BeautifulSoup(html, 'html.parser')
        if soup.find(text=re.compile("No classes were found")) == None:
            summer = True
            full_soup = soup
        else:
            summer = False

        if full_soup == None:
            return dets

        headers = full_soup.findAll("th", {
            "class": "ddtitle",
            "scope": "colgroup",
        })

        for header in headers:
            link = header.find("a").get('href')
            dets[1] = link[-5:]

        times = full_soup.findAll("table", {
            "class": "datadisplaytable",
            "summary": "This table lists the scheduled meeting times and assigned instructors for this class..",
        })

        count = 0
        for time in times:
            count += 1
            section = dict()
            split_up = [x.text for x in time.findAll("td")]
            section["class"] = split_up[0].split('<')[0]
            section["time"] = split_up[1].split('<')[0] 
            section["days"] = split_up[2].split('<')[0] 
            section["location"] = split_up[3].split('<')[0] 
            section["type"] = split_up[5].split('<')[0] 
            instructor = split_up[6].split('(')[0]
            instructor = re.sub(' +', ' ', instructor).strip()
            if instructor != "TBA":
                instructor_names = instructor.split(' ')
                if len(instructor_names) > 2 and '.' in instructor_names[1]:
                    dets[3].add(instructor_names[0] + ' ' + instructor_names[-1])
                else:
                    dets[3].add(instructor)
                section["instructor"] = instructor
            dets[2][count] = section

        search = r"""<span class="fieldlabeltext">Attributes: </span>(.*?)\n<br/>"""
        attribute = re.search(search, str(full_soup))
        tmp = attribute.group(1).strip() if attribute != None else ""
        if 'Communication Intensive' in tmp:
            dets[0] = True
            
    return dets

async def scrape_CI(years, folder_path):

    for year in tqdm(years):
        f1 = open(os.path.join(folder_path, year,'courses.json'), 'r')
        courses = json.load(f1)
        f1.close()
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=5)) as session:
            for course in courses:
                dets = await get_details(courses[course]['ID'], courses[course]['subj'], year, session)
                courses[course]['properties']['CI'] = dets[0]
                courses[course]['crn'] = dets[1]
                courses[course]['sections'] = dets[2]
                courses[course]['professors'] = list(dets[3])
        f2 = open(os.path.join(folder_path, year,'courses.json'), 'w')
        json.dump(courses, f2, sort_keys=True, indent=2, ensure_ascii=False)
        f2.close()

