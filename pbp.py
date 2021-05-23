import pandas as pd
import csv

final_season=2020
current_season=2020
all_dfs=[]

while final_season>=current_season:  
    reg_pbp_df=pd.read_csv('https://github.com/guga31bb/nflfastR-data/blob/master/data/' \
                         'play_by_play_' + str(current_season) + '.csv.gz?raw=True',
                         compression='gzip', low_memory=False)
    
    all_dfs.append(reg_pbp_df)
    
    reg_pbp_df.to_csv('pbp_{0}.csv'.format(current_season))
    current_season+=1

all_seasons=pd.concat(all_dfs)
all_seasons.to_csv('2020-now_pbp.csv')


#all_files=['pbp_2006.csv','pbp_2007.csv','pbp_2008.csv',
 #           'pbp_2009.csv','pbp_2010.csv','pbp_2011.csv',
  #          'pbp_2012.csv','pbp_2013.csv','pbp_2014.csv',
   #         'pbp_2015.csv','pbp_2016.csv','pbp_2017.csv',
    #        'pbp_2018.csv','pbp_2019.csv','pbp_2020.csv']

#combined_pbp = pd.concat([pd.read_csv(x,header=None) for x in all_files])
#combined_pbp.head()
#combined_pbp.to_csv( "2006-now_pbp", quotechar='"', quoting=csv.QUOTE_ALL, index=False, encoding='utf-8')