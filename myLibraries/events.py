import pandas as pd
import numpy as np

START_Y = 1989
END_Y = 2018

# return a string array with all years of the dataset
def get_str_years_event():
    return [str(year) for year in range(START_Y,END_Y+1)]

# return an int array with all years of the dataset
def get_int_years_event():
    return [int(year) for year in range(1990,2019)]

YEARS = get_str_years_event()

# get all events
def get_allEvents(events):
    return [e for e in range(1, events[-1])]

# return an array with the total number of collaboration for each year
def get_collabs_event():
    file = '../myDATA/00-collaboration_df.csv'
    collaborations_df = pd.read_csv(file)
    num_colls_by_y = []
    for i in range(len(YEARS)-1):
        y = YEARS[1:][i]
        # total number of collaborations in the given year
        num_colls_by_y.append(collaborations_df[y].sum())
    
    num_colls_by_y.insert(0,np.int64(1))
    return num_colls_by_y

# return an array with the total number of authors for each year
def get_auths_event():
    file = '../myDATA/00-collaboration_df.csv'
    collaborations_df = pd.read_csv(file)
    num_auths_by_y = []
    num_new_auths_by_y = []
    tot_auth = 0
    for i in range(len(YEARS)-1):
        y = YEARS[1:][i]
        
        # number of new authors in the given year
        num_new_auths_by_y.append(len(collaborations_df.loc[collaborations_df["start_year"] == int(y)]))
        
        # total number of new authors in the given year
        tot_auth += num_new_auths_by_y[i]                         
        num_auths_by_y.append(tot_auth)
        
    num_auths_by_y.insert(0,np.int64(1))
    return num_auths_by_y

# return an array with the total number of publications for each year
def get_pubs_event():
    file = '../myDATA/00-publication_df.csv'
    publication_df = pd.read_csv(file)
    num_pubs_by_y = []
    YEARS = [str(year) for year in range(1990,2019)]  
    for i in range(len(YEARS)-1):
        y = YEARS[i]
        # total number of publication in the given year
        if(i==0):
            num_pubs_by_y.append(publication_df[y].sum())
        else:
            num_pubs_by_y.append(publication_df[y].sum() + num_pubs_by_y[i-1])

    num_pubs_by_y.insert(0,np.int64(1))
    return num_pubs_by_y







########### ACTIVE EVENTS ##############

# return an array with the total number of collaboration for each year
def get_collabs_eventACTIVE(hs, act, mPubs):
    file = '../myDATA/00-collaboration_df.csv'
    collaborations_df = pd.read_csv(file)
    collaborations_df = collaborations_df[collaborations_df["max_hole_size"] <= hs]
    collaborations_df = collaborations_df[collaborations_df["activity"] >= act]
    collaborations_df = collaborations_df[collaborations_df["max_hole_size"] >= mPubs]
    num_colls_by_y = []
    for i in range(len(YEARS)-1):
        y = YEARS[1:][i]
        # total number of collaborations in the given year
        num_colls_by_y.append(collaborations_df[y].sum())
    
    num_colls_by_y.insert(0,np.int64(1))
    return num_colls_by_y

# return an array with the total number of authors for each year
def get_auths_eventACTIVE(hs, act, mPubs):
    file = '../myDATA/00-collaboration_df.csv'
    collaborations_df = pd.read_csv(file)
    collaborations_df = collaborations_df[collaborations_df["max_hole_size"] <= hs]
    collaborations_df = collaborations_df[collaborations_df["activity"] >= act]
    collaborations_df = collaborations_df[collaborations_df["max_hole_size"] >= mPubs]
    
    
    
    num_auths_by_y = []
    num_new_auths_by_y = []
    tot_auth = 0
    for i in range(len(YEARS)-1):
        y = YEARS[1:][i]
        
        # number of new authors in the given year
        num_new_auths_by_y.append(len(collaborations_df.loc[collaborations_df["start_year"] == int(y)]))
        
        # total number of new authors in the given year
        tot_auth += num_new_auths_by_y[i]                         
        num_auths_by_y.append(tot_auth)
        
    num_auths_by_y.insert(0,np.int64(1))
    return num_auths_by_y

# return an array with the total number of publications for each year
def get_pubs_eventACTIVE(hs, act, mPubs):
    file = '../myDATA/00-publication_df.csv'
    publication_df = pd.read_csv(file)
    publication_df = publication_df[publication_df["max_hole_size"] <= hs]
    publication_df = publication_df[publication_df["activity"] >= act]
    publication_df = publication_df[publication_df["max_hole_size"] >= mPubs]
    
    num_pubs_by_y = []
    YEARS = [str(year) for year in range(1990,2019)]  
    for i in range(len(YEARS)-1):
        y = YEARS[i]
        # total number of publication in the given year
        if(i==0):
            num_pubs_by_y.append(publication_df[y].sum())
        else:
            num_pubs_by_y.append(publication_df[y].sum() + num_pubs_by_y[i-1])

    num_pubs_by_y.insert(0,np.int64(1))
    return num_pubs_by_y
