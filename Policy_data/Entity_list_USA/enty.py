import pandas as pd
import requests

# URL of the HTML page containing the table
url = 'https://www.ecfr.gov/api/renderer/v1/content/enhanced/2023-12-05/title-15?subtitle=B&chapter=VII&subchapter=C&part=744&appendix=Supplement%20No.%204%20to%20Part%20744'

# Send an HTTP GET request to fetch the HTML content
response = requests.get(url)
html_content = response.text
# Read the HTML table into a DataFrame
table = pd.read_html(html_content)[0]  # Assuming the table is the first one on the page

# Save the DataFrame to an Excel file
table.to_excel('./Policy_data/Entity_list_USA/commerce.xlsx', index=False)