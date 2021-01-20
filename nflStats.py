import pandas as pd
import matplotlib.pyplot as plt
import os
import urllib.request
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import seaborn as sns
import plotly.tools as tls

##Getting Play by Play Data##
year=2020
data = pd.read_csv('https://github.com/guga31bb/nflfastR-data/blob/master/data/' \
                         'play_by_play_' + str(year) + '.csv.gz?raw=True',
                         compression='gzip', low_memory=False)


##For multiple szns just need to itearte through list of years with this for loop##
#YEARS = [2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006]




##csv already cleaned to I don't need these columns##
data.drop(['passer_player_name', 'passer_player_id',
           'rusher_player_name', 'rusher_player_id',
           'receiver_player_name', 'receiver_player_id'],
          axis=1, inplace=True)

##average epa for each team##
sort_epa=data.groupby('posteam')[['epa']].mean()

##single game pbp code##
gb_car=data.loc[(data.home_team=="GB" ) & (data.away_team=="CAR")]

##sorting qbs by overall epa and displaying cmp % over expected##
qbs = data.groupby(['passer','posteam'], as_index=False).agg({'epa':'mean',
                                                              'cpoe':'mean',
                                                              'play_id':'count'})

qbs = qbs.loc[qbs.play_id>199]
                                                            
qbs.sort_values('epa', ascending=False, inplace=True)
qbs.columns = ['Player','Team','EPA per Dropback','CPOE','Dropbacks']
#print(qbs)

##plotting epa histogram based on the play type##

#create variables for rush epa and pass epa#
rush_epa = data.epa.loc[data.play_type=='run']
pass_epa = data.epa.loc[data.play_type=='pass']

#line to create figure#
plt.figure(figsize=(16,12))

#line to create pass histogram#
plt.hist(pass_epa, bins=30, label='Pass', color='red')

#line to create rush histogram#
plt.hist(rush_epa, bins=25, label='Run', alpha=0.6, color='grey')

#lines for labels and plot title#
plt.xlabel('EPA',fontsize=14)
plt.ylabel('# of Plays',fontsize=14)
plt.title('EPA Distribution on Whether the Play is a Run or a Pass for the 2020 NFL Season',fontsize=14)
plt.figtext(.8,.04,'Ankith Kodali', fontsize=14)
plt.legend()

#figure as a png#
#plt.savefig('epa_dist.png', dpi=800)


##graph of pass rate on first down when win probability is between 25 and 75% and not in the final 2 minutes of a half##

#sorted data for this first down scenario#
first=data[['down','half_seconds_remaining','wp','posteam','pass']]
print(first)
first_down_pass_data = data.loc[(data.down<2) & (data.half_seconds_remaining>120) &
                             (data.wp>=0.25) & (data.wp<=0.75)]
print(first_down_pass_data)

teams = first_down_pass_data.groupby('posteam')[['pass']].mean()
print(teams)
teams.sort_values('pass',ascending=False,inplace=True)

#bar chart creation#
fig, ax = plt.subplots(figsize=(25,15))
ax.bar(np.arange(0,32),teams['pass'],color="black",width=.5)
ax.grid(zorder=0,alpha=.6,axis='y')
ax.set_axisbelow(True)
ax.set_xticks(np.arange(0,32))
ax.set_xticklabels(teams.index,fontsize=16)
ax.set_yticklabels([0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7],fontsize=16)

ax.set_ylabel('Pass Rate',fontsize=20,labelpad=20)
ax.set_title('1st Down Pass Rate when the Win Probability is between 25-75% (Last Two Minutes of Halves Excluded)',
             fontsize=26,pad=20)
plt.figtext(.85,.05,'Ankith Kodali',fontsize=26)
#plt.savefig('firstDownPassRate.png',dpi=400)

##air yards code to see who goes deep##
air_yards_data = (data.groupby(['receiver','posteam'])[['air_yards']]
    .sum()
    .reset_index()
    .sort_values(by=['air_yards'],ascending=False)
    .reset_index(drop=True)
    )

print(air_yards_data.head(20))

##carries inside the five yard line cause fantasy gold maybe??##

inside_five = data[
                (data.yardline_100<5) &
                (data.play_type=='run')
                ]

carries_five = (
    inside_five.groupby(['rusher','posteam'])[['play_id']]
    .count()
    .reset_index()
    .sort_values(by=['play_id'],ascending=False)
    .reset_index(drop=True)
    )

print(carries_five.head(20))
