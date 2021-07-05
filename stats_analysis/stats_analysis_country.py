import pandas as pd
import csv



# PROVIDE COUNTRY OF INTEREST
country = 'United States'



# Loading all collected infos 
df = pd.read_csv('github_accounts.csv', delimiter = ',')
df = df.drop(labels = 'Unnamed: 0', axis = 1)



# Extracting each location source that uniquely explains location and grouping by
github_loc = df[(df['github_country'] == country) & (df['github_state'].notnull())]
github_loc = github_loc[['github_state']].groupby(['github_state']).agg({'github_state': ['count']}).reset_index()
github_loc.columns = github_loc.columns.map('_'.join)
github_loc.columns = ['nuts3','github_count']

twitter_loc = df[(df['twitter_country'] == country) & (df['twitter_state'].notnull())]
twitter_loc = twitter_loc[['twitter_state']].groupby(['twitter_state']).agg({'twitter_state': ['count']}).reset_index()
twitter_loc.columns = twitter_loc.columns.map('_'.join)
twitter_loc.columns = ['nuts3','twitter_count']



# Merging the datasets
export = github_loc.merge(twitter_loc, how = 'outer')



# Some fine work on the df
export = export.fillna(0)
export[['github_count', 'twitter_count']] = export[['github_count', 'twitter_count']].astype(int)



# Summing up locations of all 
export['total'] = export['github_count'] + export['twitter_count']



# Exporting stats
export = export.sort_values(by=['total'], ascending=False)
export.to_csv('%s_country_stats.csv' % country, sep=',')





