import json
from myLibraries.events import *

            ##### RAW DATA QUERIES FOR COMPUTER SCIENCE#####

YEARS =  get_str_years_event()

# get all pubblication jsons
def get_all_raw_COMP_publications():
    all_data = []
    for y in YEARS:
        path = 'COMP/COMP/COMP-'+y+'.json'

        with open(path, 'rb') as f:
            data = json.load(f)
        
        for pub_json in data["search-results"]["entry"]:
            all_data.append(pub_json)
    return all_data

# get raw pubblication jsons for the given publication year
def get_raw_COMP_publications_by_year(year):
    path = 'COMP/COMP/COMP-'+str(year)+'.json'

    with open(path, 'rb') as f:
        data = json.load(f)

    return data["search-results"]["entry"]



