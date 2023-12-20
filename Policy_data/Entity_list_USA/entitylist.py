import xml.etree.ElementTree as ET
import pandas as pd

def parse_xml(file_path):
    # Read the XML file
    with open(file_path, 'r') as file:
        xml_data = file.read()

    # Remove the string "{http://www.un.org/sanctions/1.0}" from the XML data
    xml_data = xml_data.replace("{http://www.un.org/sanctions/1.0}", "")

    # Parse the modified XML data
    root = ET.fromstring(xml_data)

    # Create an empty list to store dataframes for each child element
    child_dfs = []

    # Define a recursive function to extract the sub-elements of a given element and store them in a dictionary
    def extract_sub_elements(element):
        data = {}
        for sub_element in element:
            sub_element_data = extract_sub_elements(sub_element)

            # Remove the string "{http://www.un.org/sanctions/1.0}" from the sub-element's name
            sub_element_name = sub_element.tag.replace("{http://www.un.org/sanctions/1.0}", "")

            # Check if the sub-element already exists in the dictionary
            if sub_element_name in data:
                # If it exists, convert the existing value to a list and append the new value
                existing_value = data[sub_element_name]
                if isinstance(existing_value, list):
                    existing_value.append(sub_element_data)
                else:
                    data[sub_element_name] = [existing_value, sub_element_data]
            else:
                # If it doesn't exist, set the value directly
                data[sub_element_name] = sub_element_data

        return data

    # Iterate over the child elements of the root element
    for child in root:
        # Extract the sub-elements of the current child element
        child_data = extract_sub_elements(child)

        # Convert the child data dictionary to a dataframe
        child_df = pd.DataFrame.from_dict(child_data, orient='index')

        # Add the child dataframe to the list
        child_dfs.append(child_df)

    # Save the dataframes into separate sheets in one Excel file
    writer = pd.ExcelWriter('./Policy_data/Entity_list_USA/commerce.xlsx', engine='xlsxwriter')
    for i, child_df in enumerate(child_dfs):
        child_df.to_excel(writer, sheet_name=f'Child {i+1}', index_label='Column Name')
    writer.save()

# Example usage
file = '/Users/mingjiexing/Desktop/Python/Tech_Innovation_war_project/Policy_data/Commerce_list/entitylist0712.xml'
parse_xml(file)