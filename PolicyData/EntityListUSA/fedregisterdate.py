import pandas as pd
from dateutil.parser import parse


## read file
file_path = 'PolicyData/EntityListUSA/FedRegisterDates2011-2023.xlsx'
df = pd.read_excel(file_path,sheet_name='Table').astype(str) 

## clean in effective date
for i in range(len(df)):
    # drop multiple effective dates
    df['Effective Date(if not date of publication)'][i] = df['Effective Date(if not date of publication)'][i].split(', except',1)[0].split(' &',1)[0].split(' (3D006 only)',1)[0]
    # fill in registers effective on publication day
    if df['Effective Date(if not date of publication)'][i] == 'nan':
        df['Effective Date(if not date of publication)'][i] = df['Publication Date'][i]
    # clean spaces
    df['Effective Date(if not date of publication)'][i] = df['Effective Date(if not date of publication)'][i].lstrip()
    # standardize date format
    d = parse(df['Effective Date(if not date of publication)'][i])
    df['Effective Date(if not date of publication)'][i] = d.strftime("%m-%d-%Y")

# drop unnecessary columns
df = df.drop(['End of Comment Period','Publication Date'],axis=1)

# drop extra spaces in fed citation
df['Federal Register Citation'] = df['Federal Register Citation'].str.strip()

# save in new sheet
with pd.ExcelWriter(file_path,
                    engine='openpyxl',
                    mode = 'a',
                    if_sheet_exists='replace') as writer:
    df.to_excel(writer,sheet_name='Table_cleaned',index=False)
