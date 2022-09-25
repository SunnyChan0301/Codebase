## order by 
# select * from airport_freq where airport_ident = 'KLAX' order by type desc
airport_freq[airport_freq.airport_ident == 'KLAX'].sort_values('type', ascending=False)

