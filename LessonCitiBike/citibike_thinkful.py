
# coding: utf-8

# In[53]:

import requests
import pandas as pd
import numpy as np
import sqlite3 as lite
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt
import time
from dateutil.parser import parse
import collections

get_ipython().magic(u'matplotlib inline')


# In[2]:

r = requests.get('http://www.citibikenyc.com/stations/json')


# In[21]:

r.json()['stationBeanList']


# See how many stations there are in the data set

# In[17]:

len(r.json()['stationBeanList'])


# Create list of keys

# In[19]:

key_list = []
for station in r.json()['stationBeanList']:
    for k in station.keys():
        if k not in key_list:
            key_list.append(k)
print(key_list)


# “Normalize” semi-structured JSON data into a flat table

# In[22]:

df = json_normalize(r.json()['stationBeanList'])


# In[23]:

df.head()


# In[27]:

df[df.statusValue == "In Service"]['availableBikes'].hist()


# In[29]:

df[df.statusValue == "Not In Service"]['availableBikes'].hist()


# In[28]:

df.statusValue.unique()


# In[30]:

df.totalDocks.mean()


# In[31]:

df[df.statusValue == 'In Service'].totalDocks.mean()


# In[32]:

df[df.statusValue == 'Not In Service'].totalDocks.mean()


# Begin storing data into SQLite3

# In[44]:

sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"


# In[47]:

con = lite.connect('citibike.db')
cur = con.cursor()

with con:
    for station in r.json()['stationBeanList']:
        cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))


# In[48]:

station_ids = df['id'].tolist() 


# In[49]:

station_ids


# In[50]:

station_ids = ['_' + str(x) + ' INT' for x in station_ids]


# In[51]:

station_ids


# In[52]:

with con:
    cur.execute("CREATE TABLE available_bikes ( execution_time INT, " +  ", ".join(station_ids) + ");")


# In[54]:

exec_time = parse(r.json()['executionTime'])


# In[55]:

exec_time


# In[56]:

with con:
    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))


# In[57]:

id_bikes = collections.defaultdict(int)


# In[58]:

id_bikes


# In[59]:

for station in r.json()['stationBeanList']:
    id_bikes[station['id']] = station['availableBikes']


# In[60]:

id_bikes


# In[61]:

with con:
    for k, v in id_bikes.iteritems():
        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")


# In[ ]:



