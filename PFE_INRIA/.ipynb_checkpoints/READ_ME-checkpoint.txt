
00: output the cumulative collaboration dataset for French computer science authors
        
        -> myDATA/00-collaboration_df.csv
    
05: output one subset of collaboration_df for each possible hole length in pubblication 
        
        -> myDATA/05-filtered_by_hole_size/filtered_by_hole_size_<SIZE>.csv
    
10: split each collaboration dataset of '05' by starting collaboration year
        
        -> myDATA/10-splitted_by_hole_size_<SIZE>/collabs_by_year_<YEAR>.csv

15: plot the top 100 collaborators trajectories of '10' for each splitted dataset 
        
        -> myDATA/10-splitted_by_hole_size_<SIZE>/plt/<YEAR>_holeSize_<SIZE>.png

20: plot the average trajectory of '10' for each splitted dataset 
        
        -> myDATA/10-splitted_by_hole_size_<SIZE>/plt_avg/<YEAR>_holeSize_<SIZE>.png
 
25: plot functions on pubblication dataset
        
        -> x=years, y=#new_authors
        -> x=years, y=#new_pubblication

30: output the number of authors that have stopped collaborating in the given year, for each year

32: output the number of authors, who appears in the collaboration dataset, that have stopped publishing in the given year, for each year

35: plot rations beetween quantities from collaboration dataset:
         
         -> x=years                 , y=#collaborations/#authors
         -> x=years                 , y=#new_collaborations/#new_authors
         -> x=new_collaboration     , y=#collaborations/#authors
         -> x=new_collaboration     , y=#new_collaborations/#new_authors
