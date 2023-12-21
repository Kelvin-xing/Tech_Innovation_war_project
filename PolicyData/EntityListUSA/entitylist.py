## This code extracts Code of Federal Regulations Supplement No. 4 to Part 744, Title 15, from https://www.ecfr.gov/current/title-15/part-744/appendix-Supplement No. 4 to Part 744
## It contains the list of names of certain non-US entities that are subject to specific license requirements for export, re-export or transfer of specified items by bureau of industry and security, US Department of Commerce
## For more details, check https://www.bis.doc.gov/index.php/policy-guidance/lists-of-parties-of-concern/entity-list


import pandas as pd
from bs4 import BeautifulSoup
import os

# This function extracts the table from the html version of the entity list, clean it into an unbalanced panel and save into an excel
def Commerce_list_extract(xml_file):
    """
    This function extracts a table from an XML file, converts it into a DataFrame,
    and saves it as a CSV file.
    """
    # Load XML file
    with open(xml_file, 'r') as file:
        xml_data = file.read()

    # Parse XML data
    soup = BeautifulSoup(xml_data, 'xml')

    # Find table element
    table = soup.find('table')

    # Extract rows and cells from table
    rows = table.find_all('tr')
    table_data = []
    for row in rows:
        cells = row.find_all('td')
        row_data = []
        for cell in cells:
            row_data.append(cell.get_text().strip())
        table_data.append(row_data)

    # Convert table data into a DataFrame
    df = pd.DataFrame(table_data)

    # Save DataFrame as CSV file
    csv_file = 'EntityListCommerce' + os.path.splitext(xml_file)[48:59]+ '.csv'
    df.to_csv(csv_file, index=False)

    return df

file = 'https://drafting.ecfr.gov/api/versioner/v1/full/2023-12-19/title-15.xml?appendix=Supplement+No.+4+to+Part+744&part=744'
Commerce_list_extract(file)
