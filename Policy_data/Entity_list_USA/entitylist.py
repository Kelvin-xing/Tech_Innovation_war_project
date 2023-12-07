url = 'https://www.ecfr.gov/api/versioner/v1/structure/2023-11-06/title-15.json'


import pandas as pd
import json

# Read JSON from URL
response = pd.read_json(url)

# Normalize the "children" field
data = json.loads(response.to_json(orient='records'))
df = pd.json_normalize(data, 'children', ['id', 'name'])


# Save DataFrame to XLSX file
df.to_excel('./Policy_data/Entity_list_USA/entitylist.xlsx', index=False)