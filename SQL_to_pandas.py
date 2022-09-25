## order by 
# select * from airport_freq where airport_ident = 'KLAX' order by type desc
airport_freq[airport_freq.airport_ident == 'KLAX'].sort_values('type', ascending=False)

## group by count
# select iso_country, type, count(*) from airports group by iso_country, type order by iso_country, type
airports.groupby(['iso_country', 'type']).size().to_frame('size').reset_index()
airports.groupby(['iso_country', 'type']).size()\
.to_frame('size').reset_index().sort_values(['iso_country', 'size'], ascending=[True, False])

## having
# select type, count(*) from airports where iso_country = 'US' group by type having count(*) > 1000 order by count(*) desc
airports[airports.iso_country == 'US'].groupby('type')\
.filter(lambda g: len(g) > 1000).groupby('type').size().sort_values(ascending=False)

## Group by agg
airport_freq.groupby(['type','description']).agg({'frequency_mhz':'max'}).reset_index()
airport_freq[airport_freq['airport_ident']=='01FL'].groupby(['type','description']).agg({'frequency_mhz':'max'}).reset_index()

## distinct count
airport_freq[['type','description']].drop_duplicates().shape

## rename
airport_freq.rename(columns={'type': 'type2'})

## Concat Col and fill na
airport_freq['type']=airport_freq['type'].fillna('')
airport_freq['description']=airport_freq['description'].fillna('')
airport_freq['new']=airport_freq['type']+'-'+airport_freq['description']
airport_freq['new']=airport_freq[['type','description']].apply("-".join, axis=1)

## Cast astype
airport_freq = airport_freq.astype({"type":"string","description":"string"})

## NP Ceil 
airport_freq['frequency_mhz']=np.int16(np.ceil(airport_freq['frequency_mhz']))

## Case when
# np.select
conditions=[
    (airport_freq['type']=='CTAF') & (airport_freq['airport_ident']=='00CA'),
    airport_freq['frequency_mhz'].between(100,200),
    np.ceil(airport_freq['frequency_mhz']).between(100,200)
]
value=['500','AAA','BBB']
airport_freq['casewhen']=np.select(conditions, value, default=np.nan)
# np.where
airport_freq['casewhen']=np.where(airport_freq['airport_ident']=='00CA',500,100)
airport_freq['casewhen']=np.where((airport_freq['type']=='CTAF') & (airport_freq['airport_ident']=='00CA'),500,100)
# np.where2
airport_freq['class'] =   np.where(airport_freq['description'].isna(), 'Bad',
                          np.where((airport_freq['type']=='CTAF') & (airport_freq['airport_ident']=='00CA'), 'OK',
                          np.where(np.ceil(airport_freq['frequency_mhz']).between(100,200), 'Good', 'Great')))


## Left join 
airport_freq.merge(airports,how='left',left_on=['id','airport_ident','type'],right_on=['id','ident','type'])

## sqlite3
import pandas as pd
import sqlite3

airport_freq = pd.read_csv('data/airport-frequencies.csv')
conn = sqlite3.connect('test.db')  #建立資料庫
cursor = conn.cursor()
cursor.execute('CREATE TABLE airport_freq(id, airport_ref, airport_ident, type, description,frequency_mhz)')  #建立資料表
conn.commit()

airport_freq.to_sql('airport_freq', conn, if_exists='replace', index=False) 

pd.read_sql("""
select count(id)
,max(frequency_mhz)
from airport_freq
""", conn)









