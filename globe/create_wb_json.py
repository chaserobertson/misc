import csv, json
import pandas as pd
import world_bank_data as wb

pd.set_option('display.max_rows', 12)

# Countries and associated regions
countries = wb.get_countries()

# Population dataset, indexed with the country code
population = wb.get_series('SP.POP.TOTL', id_or_value='id', simplify_index=True, mrv=1)

# Aggregate region, country and population
df = countries[['region', 'name']].rename(columns={'name': 'country'}).loc[countries.region != 'Aggregates']
df['population'] = population

regions_list = set(df['region'].to_list())
region_clusters = { region: [] for region in regions_list }

for row in df.itertuples():
    if row.country and row.population > 10:
        region_clusters[row.region].append({
            'name': row.country,
            'value': row.population
        })

out_dict = {
    'name': 'globe',
    'children': [
        {
            'name': region,
            'children': region_clusters[region]
        }
    for region in regions_list
    ]
    }

out_json = json.dumps(out_dict)
with open('globe2.json', 'w') as out_file:
    out_file.write(out_json)