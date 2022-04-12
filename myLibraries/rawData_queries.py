import json
from myLibraries.events import *

            ##### RAW DATA QUERIES FOR COMPUTER SCIENCE#####

YEARS =  get_str_years_event()[1:]

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

JSON = get_all_raw_COMP_publications() # retrieve all json of computer science publication 

# get all COMP publications for the given author
def get_COMP_publications_by_authID(authID):
    authID = str(authID)
    auth_pubs = [] # publications already checked for the current author
    for pub in JSON:
        if("author" in pub):
            auths = pub["author"] # authors of the current publication
            
            if(type(auths) == dict):
                auth = auths
                if(auth["authid"] == authID):
                    if(pub not in auth_pubs):
                        auth_pubs.append(pub)
                
            elif(type(auths) == list):
                for auth in auths:
                    if(auth["authid"] == authID):
                        if(pub not in auth_pubs):
                            auth_pubs.append(pub)
    return auth_pubs

# get all COMP publications for the given author and year
def get_COMP_publication_by_authID_and_year(authID, year):
    auth_pubs = get_COMP_publications_by_authID(authID)
    pubs_y = []
    for pub in auth_pubs:
        if("prism:coverDate" in pub):
            if (pub["prism:coverDate"][:4]==year):
                pubs_y.append(pub)
        elif("prism:coverDisplayDate" in pub):
            if (pub["prism:coverDisplayDate"][-4:]==year):
                pubs_y.append(pub)
    return pubs_y

# get start and end year of COMP authors given their id
def get_COMP_start_and_end_year_by_authID(authID):
    auth_pubs = get_COMP_publications_by_authID(authID)
    pubs_years = set()
    for pub in auth_pubs:
        if("prism:coverDate" in pub):
            if(type(pub["prism:coverDate"]) == str):
                year = int(pub["prism:coverDate"][:4])
            else:
                year = int(pub["prism:coverDate"][0][:4])
            pubs_years.add(year)
        elif("prism:coverDisplayDate" in pub):
            if(type(pub["prism:coverDisplayDate"]) == str):
                year = int(pub["prism:coverDisplayDate"][-4:])
            else:
                year = int(pub["prism:coverDisplayDate"][0][-4:])
            pubs_years.add(year)
    
    if(pubs_years != set()):
        return min(pubs_years), max(pubs_years)
    
    return 0,0

# return the publication trajectory for each the given author
def get_COMP_publication_traj_size_by_authID(authID):
    auth_pubs = get_COMP_publications_by_authID(authID)
    
    publication_traj = [0 for i in YEARS]

    i = 0
    for y in YEARS:
        for pub in auth_pubs:
            year  = ""
            if("prism:coverDate" in pub):
                if(type(pub["prism:coverDate"]) == str):
                    year = int(pub["prism:coverDate"][:4])
                else:
                    year = int(pub["prism:coverDate"][0][:4])
            elif("prism:coverDisplayDate" in pub):
                if(type(pub["prism:coverDisplayDate"]) == str):
                    year = int(pub["prism:coverDisplayDate"][-4:])
                else:
                    year = int(pub["prism:coverDisplayDate"][0][-4:])

            if(str(year) == y):
                publication_traj[i] = publication_traj[i] + 1 
                
        i += 1

    return publication_traj

# return the maximum hole size for an author
def get_COMP_max_hole_size_by_authID(authID):
    traj = get_COMP_publication_traj_size_by_authID(authID)
    
    max_hole = 0
    c=0
    
    for deg in traj:
        if(deg==0):
            c += 1
        else:
            if(c > max_hole):
                max_hole = c
            c = 0   
    if(c > max_hole):
                max_hole = c

    return max_hole