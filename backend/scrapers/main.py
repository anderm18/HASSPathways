import os
import json
from tqdm import tqdm
import frontend_pathway_scraper as path_scraper
'''
New scraping main file as of Summer 2024. All files except frontend_pathway_scraper.py are deprecated, 
because the old api key for the catalog is no longer valid.

Currently, this only scrapes the most recent year, so when you run this file for a new semester change the year to the
newest catalog so that it outputs to the correct folder.

This file will scrape the pathways and verify the output. Check verify.txt for the differences between the old and new pathways files.

To do a static verification (dont change the old pathways file), run frontend_pathway_scraper.py directly.
I would highly suggest doing that first if you make any changes to frontend_pathway_scraper.py.
'''
if __name__ == "__main__":
    year = "2024-2025"
    previous_year = "2023-2024"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = os.path.dirname(os.path.dirname(dir_path))
    json_path = os.path.join(parent_path, "frontend", "src", "data", "json")
    path = os.path.join(json_path, str(year))
    new_year = True
    try:
        # Make dir if does not already exist
        os.mkdir(path)
    except Exception:
        print(f"Folder for {str(year)} already made")
        new_year = False
    pathway_loc = os.path.join(path, 'pathways.json')
    
    old_pathway_loc = os.path.join(path, 'pathways_old.json')
    verify_loc = os.path.join(path, 'verify.txt')
    try:
        f = open(pathway_loc, 'r')
    except FileNotFoundError:
        f = open(pathway_loc, 'w')
        f.write('{}')
        f.close()
        f = open(pathway_loc, 'r')
    f_old = open(old_pathway_loc, 'w')
    # copy the previous pathways file to pathways_old.json
    f_old.write(f.read())
    f_old.close()
    f.close()
    path_scraper.scrape_all(pathway_loc)
    if new_year:
        old_pathway_loc = os.path.join(json_path, previous_year, 'pathways.json')
    path_scraper.verify_output(pathway_loc, old_pathway_loc, verify_loc)
    

   