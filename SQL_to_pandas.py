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

## 

