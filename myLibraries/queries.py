import pandas as pd
import os
import numpy as np
from myLibraries.events import *

YEARS = get_str_years_event()

            ##### GENERAL DATA QUERIES #####

# get the names of all authors along with theri IDs
def get_all_COMP_names():
    file = "../myDATA/02-names.csv"
    if(os.path.exists(file)):
        return pd.read_csv(file)
    return -1

# get the names of all authors along with theri IDs
def get_COMP_names_by_start_year(year):
    file = "../myDATA/02-names.csv"
    if(os.path.exists(file)):
        df = pd.read_csv(file)
        df_y = df[df["start_year"] == year]
        return df_y
    return -1

# get the ending publication year for each author
def get_ending_years():
    file = "../myDATA/03-ending_years.csv"
    if(os.path.exists(file)):
        df = pd.read_csv(file)
        return df
    return -1

# get the starting publication year for each author
def get_starting_years():
    file = "../myDATA/03-starting_years.csv"
    if(os.path.exists(file)):
        df = pd.read_csv(file)
        return df
    return -1

# get the starting and ending publication year for each author
def get_starting_and_ending_years():
    end_y = get_ending_years()
    start_y = get_starting_years()
    return pd.merge(start_y, end_y)


            ##### PUBLICATION DATA QUERIES #####

'''# get all publication data
def get_all_pubs():
    file = "../myDATA/01-publication_df_with_starting_years.csv"
    if(os.path.exists(file)):
        return pd.read_csv(file)
    return -1'''
    
            ##### COLLABORATION DATA QUERIES #####

# get all collaboration data
def get_all_collabs():
    file = "../myDATA/00-collaboration_df.csv"
    if(os.path.exists(file)):
        return pd.read_csv(file)
    return -1

# get all collaboration data for given hole size
def get_all_collabs_by_hole_size(size):
    df = get_all_collabs()
    df = df[df["max_hole_size"] <= size]
    return df

# get all collaboration data for given hole size and starting year
def get_collabs_by_hole_size(size, start_y):
    
    df = get_all_collabs_by_hole_size(size) # get authors by HS
    df = df[df["start_year"] == int(start_y)] # get all raws with the given starting year
    
    # remove from it the usless years
    preceding_years = YEARS[1:YEARS.index(str(start_y))]
    df = df[df.columns.difference(preceding_years)]
    
    return df

# return the average trajectory for the given hole size and starting publication year
def get_avg_trajectories(events, hole_size, start_y, section=0):
    start_y = int(start_y) + 1
    
    df_y = get_collabs_by_hole_size(hole_size, start_y)
    
    j=YEARS.index(str(start_y))
        
    x,y = [], []
    for i in df_y:
        if(i in YEARS):
            y.append(df_y[i].mean())
            x.append(events[j])
            j+=1
    
    x.insert(0, events[YEARS.index(str(start_y))-1])
    y.insert(0,1)
    
    if(section != 0):
        return x[:section], y[:section]
    
    return x, y


            ##### FUNDING DATA #####

#return all granted and not granted data
def get_all_granting_data():
    file = "../myDATA/grantingDATA/00-granting_DATA.csv"
    if(os.path.exists(file)):
        return  pd.read_csv(file)
    return -1

#return granted data
def get_granted():
    file = "../myDATA/grantingDATA/01-granted.csv"
    if(os.path.exists(file)):
        return  pd.read_csv(file)
    return -1

#return not granted data
def get_not_granted():
    file = "../myDATA/grantingDATA/01-not_granted.csv"
    if(os.path.exists(file)):
        return  pd.read_csv(file)
    return -1

# return all group IDs 
def get_all_groups():
    return get_all_granting_data()["group"]

# return thos focaal control groups of which memeber have a distance less equal than the given one between their starting years
def get_groups_by_dist(d):
    foc_con = get_all_granting_data() # funding data for which we have collaboration data and for each focal we have a control
    granted = get_granted() # get just the granted data
    not_granted = get_not_granted() #get just the not granted data

    chosen_groups = []
    for g in foc_con["group"]:
        foc_start_y = granted[granted["group"] == g]["start_year"].values[0]
        con_start_y = not_granted[not_granted["group"] == g]["start_year"].values[0]
        dist = abs(foc_start_y - con_start_y)
        if(dist <= d):
            chosen_groups.append(g)
    
    return chosen_groups    
    
# return trajectories for focal and control of the given group along with their IDs and the granting year
def get_focal_control_traj_byGroup(groupID):
    foc_con = get_all_granting_data()
    
    focal = foc_con.loc[(foc_con['group'] == groupID) & (foc_con['focal'] ==1)]
    focal_ID = str(focal.iloc[0]["ID"])
    focal_start_y = focal["start_year"].values[0]
    grant_year = str(focal.iloc[0]["anr_year"])

    control = foc_con.loc[(foc_con['group'] == groupID) & (foc_con['focal'] ==0)]
    control_ID = str(control.iloc[0]["ID"])
    control_start_y = control["start_year"].values[0]
    
    y_focal, y_control = [0], [0]
    for i in YEARS[1:]:
        j=YEARS.index(i)
        
        if(i==focal_start_y):
            y_focal.append(1)
        else:
            y_focal.append(focal[i])
            
        if(i==control_start_y):
            y_control.append(1)
        else:
            y_control.append(control[i])
            
    return focal_ID, control_ID, y_focal, y_control, grant_year

# return average trajectory for focals by starting year
def get_focals_avg_trajectories(events, start_y, start_y_dist=-1):
    
    if(start_y_dist==-1):
        considered_groups = get_all_groups()
    else:
        considered_groups = get_groups_by_dist(start_y_dist)
    
    start_y = str(int(start_y)+1)
    
    df_y = get_granted()
    df_y = df_y[df_y.group.isin(considered_groups)]
    df_y = df_y[df_y["start_year"]==int(start_y)]
    
    if(len(df_y)==0):
        return  [], []
    
    j=YEARS.index(start_y)

    x,y = [], []
    for i in YEARS[YEARS.index(start_y):]:
        y.append(df_y[i].mean())
        x.append(events[j])
        j+=1
    
    x.insert(0, events[YEARS.index(str(start_y))-1])
    y.insert(0,1)
        
    return x, y

# get average trajectory for controls by starting year
def get_controls_avg_trajectories(events, start_y, start_y_dist=-1):
    
    if(start_y_dist==-1):
        considered_groups = get_all_groups()
    else:
        considered_groups = get_groups_by_dist(start_y_dist)
    
    start_y = str(int(start_y)+1)
    
    df_y = get_not_granted()
    df_y = df_y[df_y.group.isin(considered_groups)]
    df_y = df_y[df_y["start_year"]==int(start_y)]
    
    
    if(len(df_y)==0):
        return  [], []
    
    j=YEARS.index(start_y)

    x,y = [], []
    for i in YEARS[YEARS.index(start_y):]:
        y.append(df_y[i].mean())
        x.append(events[j])
        j+=1
    
    x.insert(0, events[YEARS.index(str(start_y))-1])
    y.insert(0,1)
        
    return x, y
