import courses_scraper
import pathway_scraper
import fill_empty
import sis_scraper
import category_assembler
import rmp_scraper
import asyncio
import os
import json
from tqdm import tqdm

if __name__ == "__main__":
    years = list(map(lambda x: x[0], courses_scraper.get_catalogs()))
    print(years)
    #years = [x[:4] for x in years]
    all_courses = courses_scraper.scrape_courses()
    print(all_courses)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = os.path.dirname(os.path.dirname(dir_path))
    json_path = os.path.join(parent_path, "frontend", "src", "data", "json")
    for year in tqdm(years):
        path = os.path.join(json_path, str(year))
        try:
            # Make dir if does not already exist
            os.mkdir(path)
        except Exception:
            print(f"Folder for {str(year)} already made")
        f = open(os.path.join(path, 'courses.json'), 'w')
        json.dump(all_courses[year], f, sort_keys=True, indent=2, ensure_ascii=False)
        f.close()

    print("Started scraping CI courses")
    asyncio.run(sis_scraper.scrape_CI(years, json_path))
    print("Finished scraping CI courses")

    all_pathways = pathway_scraper.scrape_pathways()
    print(years)
    for year in years:
        path = os.path.join(json_path, str(year))

        f = open(os.path.join(path, 'pathways.json'), 'w')
        json.dump(all_pathways[year], f, sort_keys=True, indent=2, ensure_ascii=True)
        f.close()

    print("Starting to fill non-catalog courses")
    for year in years:
        path = json_path + str(year)
        asyncio.run(fill_empty.fill(path))
    print("Finished to fill non-catalog courses")
    
    f = open(os.path.join(json_path, 'years.json'), 'w')
    json.dump(years, f, sort_keys=True, indent=2, ensure_ascii=True)
    f.close()
    category_assembler.assemble(json_path)

    print("Started scraping RateMyProfessor")
    asyncio.run(rmp_scraper.scrape_RMP(json_path))
    print("Started scraping RateMyProfessor")
