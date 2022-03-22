import pandas as pd
import os
from myLibraries.events import *

YEARS = get_str_years_event()


            ##### PUBLICATION DATA QUERIES #####

# get all publication data
def get_all_pubs():
    file = "myDATA/01-publication_df_with_starting_years.csv.csv"
    if(os.path.exists(file)):
        return pd.read_csv(file)
    return -1


            ##### COLLABORATION DATA QUERIES #####

# get all collaboration data
def get_all_collabs():
    file = "myDATA/00-collaboration_df_with_starting_years.csv"
    if(os.path.exists(file)):
        return pd.read_csv(file)
    return -1

# get all collaboration data for given hole size
def get_all_collabs_by_hole_size(size):
    file = "myDATA/collabs_by_hole_size/" + str(size) + ".csv"
    if(os.path.exists(file)):
        return pd.read_csv(file)
    return -1

# get all collaboration data for given hole size and starting year
def get_collabs_by_hole_size(size, start_y):
    file = "myDATA/collabs_by_hole_size_and_start_year/" 
    file += str(size) + "_hole_size_splitted/"
    file += str(start_y) + "_collabs_by_starting_year.csv"
    
    if(os.path.exists(file)):
        return pd.read_csv(file)
    return -1

# return the average trajectory for the given hole size and starting publication year
def get_avg_trajectories(events, hole_size, start_y):
    
    df_y = get_collabs_by_hole_size(hole_size, start_y)
    j=YEARS.index(start_y)
        
    x,y = [], []
    for i in df_y:
        if(i!="ID"):
            y.append(df_y[i].mean())
            x.append(events[j])
            j+=1
    return x, y


            ##### FUNDING DATA #####

#return all granted and not granted data
def get_all_granting_data():
    file = "myDATA/grantingDATA/00-granting_DATA.csv"
    if(os.path.exists(file)):
        return  pd.read_csv(file, index_col=0)
    return -1

#return granted data
def get_granted():
    file = "myDATA/grantingDATA/01-granted.csv"
    if(os.path.exists(file)):
        return  pd.read_csv(file, index_col=0)
    return -1


#return not granted data
def get_not_granted():
    file = "myDATA/grantingDATA/01-not_granted.csv"
    if(os.path.exists(file)):
        return  pd.read_csv(file, index_col=0)
    return -1

# return trajectories for focal and control of the given group along with their IDs and the granting year
def get_focal_control_traj_byGroup(groupID):
    foc_con = get_all_granting_data()
    
    focal = foc_con.loc[(foc_con['group'] == groupID) & (foc_con['focal'] ==1)]
    focal_ID = str(focal.iloc[0]["auth.id"])
    grant_year = str(focal.iloc[0]["anr_year"])

    control = foc_con.loc[(foc_con['group'] == groupID) & (foc_con['focal'] ==0)]
    control_ID = str(control.iloc[0]["auth.id"])

    y_focal, y_control = [], []
    for i in YEARS:
        j=YEARS.index(i)
        y_focal.append(focal[i])
        y_control.append(control[i])
        
    return focal_ID, control_ID, y_focal, y_control, grant_year

# return average trajectory for focals by starting year
def get_focals_avg_trajectories(events, start_y):
    
    df_y = get_granted()
    df_y = df_y[df_y["start_year"]==int(start_y)]
    
    if(len(df_y)==0):
        return  [], []
    
    j=YEARS.index(start_y)

    x,y = [], []
    for i in YEARS[YEARS.index(start_y):]:
        y.append(df_y[i].mean())
        x.append(events[j])
        j+=1
        
    return x, y

# get average trajectory for controls by starting year
def get_controls_avg_trajectories(events, start_y):
    
    df_y = get_not_granted()
    df_y = df_y[df_y["start_year"]==int(start_y)]
    
    if(len(df_y)==0):
        return  [], []
    
    j=YEARS.index(start_y)

    x,y = [], []
    for i in YEARS[YEARS.index(start_y):]:
        y.append(df_y[i].mean())
        x.append(events[j])
        j+=1
        
    return x, y
