import os
import pandas as pd
import csv
import censusdata
from dotenv import load_dotenv
from key import master_key as mk
from  builtins import any as b_any


# load environment variables
load_dotenv(os.path.join('', '.env'))

CENSUS_KEY = os.getenv("CENSUS_KEY")

suffolk_id = '103'
nassau_id = '059'

bronx_id = '005'
kings_id = '047'
manhattan_id = '061'
queens_id = '081'
richmond_id = '085'

LI = [suffolk_id, nassau_id]
NYC = [bronx_id, kings_id, manhattan_id, queens_id, richmond_id]
# this is rest-of-state
ROS = ['001','003','007','009','011','013','015','017','019','021','023','025','027','029','031','033','035','037','039','041','043','045','049','051','053','055','057','063','065','067','069','071','073','075','077','079','083','087','089','091','093','095','097','099','101','105','107','109','111','113','115','117','119','121','123']

loc = {
    'LI': LI,
    'NYC': NYC,
    'ROS': ROS
}

pd.set_option('display.expand_frame_repr', False)

def update_CDP(year):
    indicators = mk['Indicators']
    for topic in indicators:
        print(topic)
        categories  = mk[topic]['categories']

        for category in categories:
            print(category)
            locations = mk[topic][category]['locations']
            master = pd.DataFrame()
            try:
                if b_any('DP' in x for x in list(mk[topic][category]['data'].keys())):
                    dict_list = censusdata.download('acs5', year, censusdata.censusgeo([('state', '36'), ('place', '*')]), list(mk[topic][category]['data'].keys()), key=CENSUS_KEY, tabletype='profile')
                else:
                    dict_list = censusdata.download('acs5', year, censusdata.censusgeo([('state', '36'), ('place', '*')]), list(mk[topic][category]['data'].keys()), key=CENSUS_KEY, tabletype='detail')

                dict_list = dict_list.rename(columns=mk[topic][category]['data'])
                master = master.append(dict_list)
                os.makedirs('automated/'+topic+'/'+category+'/src/', exist_ok=True)
                master.to_csv('automated/'+topic+'/'+category+'/src/'+str(year)+'_CDP.csv')
            except:
                pass


def update_county(year):
    indicators = mk['Indicators']
    for topic in indicators:
        print(topic)
        categories  = mk[topic]['categories']

        for category in categories:
            print(category)
            locations = mk[topic][category]['locations']
            master = pd.DataFrame()
            try:
                if b_any('DP' in x for x in list(mk[topic][category]['data'].keys())):
                    dict_list = censusdata.download('acs1', year, censusdata.censusgeo([('state', '36'), ('county', '*')]), list(mk[topic][category]['data'].keys()), key=CENSUS_KEY, tabletype='profile')
                else:
                    dict_list = censusdata.download('acs1', year, censusdata.censusgeo([('state', '36'), ('county', '*')]), list(mk[topic][category]['data'].keys()), key=CENSUS_KEY, tabletype='detail')

                dict_list = dict_list.rename(columns=mk[topic][category]['data'])
                master = master.append(dict_list)
                os.makedirs('automated/'+topic+'/'+category+'/src/', exist_ok=True)
                master.to_csv('automated/'+topic+'/'+category+'/src/'+str(year)+'_county.csv')
            except:
                pass

initial = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]
# initial = [2019]
for year in initial:
    update_county(year)

cdp_years = [2013, 2018]
for cyear in cdp_years:
    update_CDP(cyear)