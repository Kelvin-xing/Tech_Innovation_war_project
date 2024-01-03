### This code cleans Code of Federal Regulations Supplement No. 4 to Part 744, Title 15, from https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-744/appendix-Supplement%20No.%204%20to%20Part%20744
### It contains the list of names of certain non-US entities that are subject to specific license requirements for export, re-export or transfer of specified items by bureau of industry and security, US Department of Commerce
### CSV version downloadable from https://www.bis.doc.gov/index.php/documents/consolidated-entity-list?format=html
### For more details, check https://www.bis.doc.gov/index.php/policy-guidance/lists-of-parties-of-concern/entity-list

import pandas as pd
import re
from dateutil.parser import parse

## Historical revisions updated 2023-12-22
dates = ['2023-12-07','2023-11-21','2023-11-17','2023-11-06','2023-10-19','2023-10-11','2023-9-27','2023-7-19','2023-6-21','2023-6-14','2023-5-22','2023-4-26','2023-4-17','2023-3-30','2023-3-14','2023-3-06','2023-2-27','2023-2-14','2023-2-01','2022-12-23','2022-12-19','2022-12-16','2022-12-08','2022-10-21','2022-10-13','2022-10-07','2022-10-04','2022-9-16','2022-9-09','2022-8-24','2022-6-30','2022-6-06','2022-6-01','2022-5-11','2022-4-11','2022-4-07','2022-3-16','2022-3-09','2022-3-08','2022-3-03','2022-2-14','2022-2-03','2021-12-17','2021-11-26','2021-11-04','2021-10-05','2021-8-20','2021-7-21','2021-7-19','2021-7-12','2021-7-06','2021-6-24','2021-6-16','2021-6-01','2021-4-09','2021-3-16','2021-3-08','2021-3-04','2021-1-15','2020-12-23','2020-12-22','2020-10-30','2020-10-19','2020-9-22','2020-9-11','2020-8-27','2020-8-20','2020-7-22','2020-6-18','2020-6-05','2020-5-19','2020-3-16','2020-3-02','2019-12-18','2019-12-06','2019-11-13','2019-10-21','2019-10-09','2019-8-21','2019-8-14','2019-6-24','2019-5-24','2019-5-21','2019-5-14','2019-4-11','2018-12-20','2018-10-30','2018-9-26','2018-9-12','2018-9-04','2018-8-30','2018-8-01','2018-3-22','2018-2-16','2018-1-26','2017-12-20','2017-9-25','2017-6-30','2017-6-22','2017-5-26','2017-4-18','2017-3-29','2017-3-16']

## File under cleaning process
# Note: Can loop over dates
file = f"EntityList{dates[0]}.csv"
df = pd.read_csv(f"PolicyData/EntityListUSA/{file}",usecols=['Name', 'Address','City','State/Province','Country','Federal Register Notice','Effective Date','License Requirement','License Policy']).astype(str)

## Explode into panel
df = df.set_index(['Name','Address','City','State/Province','Country','License Requirement','License Policy'])
for index in range(len(df)):
    df['Effective Date'][index] = re.split(r'[;,]\s*',df['Effective Date'][index])
    df['Federal Register Notice'][index] = re.split(r'\sand\s|[;,]\s*',df['Federal Register Notice'][index])
df = df.explode('Effective Date').explode('Federal Register Notice').reset_index()


## Concatenate addresses
df['Full Address'] = df['Address'] + ' '+ df['City'] + ' ' + df['State/Province']
df = df[['Name','Country','Federal Register Notice','Effective Date','License Requirement','License Policy','Full Address']]

## Split human and company with identifier as a new column
# keywords for firm, government and research institutes
firmwords = [# Typical firm suffix
            'llc','corp','system','industr','company','ltd','co.','group','factory','enterprise','association','jsc','plant','branch','limited','llp','associates','foundation','inc','sdn bhd','development','headquarter','gmbh','limited','private','oao','ooo','zao','s.a.',' ao',' ab',' oy',
            # Geography
            'global','beijing','international',
            # Industry
                # construction and manufacture
                'construction', 'steel','engineer','metro','bridge','production','konstrukt',
                # energy
                'energy',
                # pharma
                'pharm',
                # IT
                'computer','semiconductor','electron','micro','radio','microwave','cloud','display','elec','infotec','video','tronic','chip',
                # tech in general
                'technolog','laboratory','integra','tech','solution',
                # trade
                'trad','service','export','import','logist',
                # transportation
                'aero','airline','aerospace','shipyard','ship','aircraft','flight',
                # others
                'design','field',
             # Firm specific
             'huawei', 'Moselectronproekt','nexus','proven honour','gazprom','oceanos','vad, ao','proexcom','magnetar','apex','melkom','abris','dm link','sngb ao','jadeshine','sputnik','ikco','cytrox'
             ]
institutewords = ['university','research','institute','academy']
govwords =['ministry','desto','paec','cnsim','state','federal','bureau','ukraine','intelligence']
# In question: adimir ou, sdb ire ras, elara, NPP istok, UAB Pella-Fjord, ZAO Elmiks-VS, ZAO Sparta, ZAO svyaz Inzhiniring, GBNTT, ZAO, uralvagonzavod, kalashnikov concern, aquanika, specelkom,megel mekom, aviton, arsenal,bitreit, stroygazmontazh, transoil, rosneft, surgutneftegas, Otkrytoe Aktsionernoe Obshchestvo Vneshneekonomicheskoe Obedinenie Tekhnopromeksport, angstrem-M, FAU ?Glavgosekspertiza Rossii?, Druzhba AO,FKU Uprdor ?Taman?,gazmash ao, npc granat, SMT?K,Yamalgazinvest ZAO, Institut Stroiproekt AO, bike center, concord catering, ifdk cao, Wolf' Holding of Security Structures, Sovkhoz Chervishevski PAO, Femteco, LabInvest, Interlab, Rau Farm, Regionsnab, Aktsionernoe Obshchestvo, Rostekh – Azimuth, SP Kvant, UEC-Saturn,AO Kronshtadt, Elara, ELPROM, corezing,oy

# matching type
df['Type']='Human'
for index, row in df.iterrows():
    text = row['Name']
    if any (firmword in text.lower() for firmword in firmwords):
        df.at[index,'Type']='Firm'
    if any (govword in text.lower() for govword in govwords):
        df.at[index,'Type']='Government'
    if any (instituteword in text.lower() for instituteword in institutewords):
        df.at[index,'Type']='Research Institute'

## Cleaning Name
replacer = {'Xi?an':'Xian',
            "Xi'an":'Xian'
}
df['Name'] = df['Name'].str.strip().replace(replacer)

## Clean fed registration
fc = pd.read_excel('PolicyData/EntityListUSA/UnknownFedRegister.xlsx') # fc for fed register check
# function to tell date aside from register
def split_and_parse(string):
    halves = string.split('. ')
    if len(halves) == 2:
        return halves[1]
    else:
        return halves[0]

df['Federal Register Notice'] = df['Federal Register Notice'].apply(lambda x: split_and_parse(x))

for i in range(len(df)):
    # to save only the register part
    df['Federal Register Notice'][i] = df['Federal Register Notice'][i].split(' No.',1
    )[0].split(' (',1)[0].replace(' no. 242 pg.','').strip()
    # maunally fill na
    if df['Federal Register Notice'][i] == 'nan':
        continue
        # match from fc
    else:
        continue


## Match Effective Date
# Fed Register - Effective date 2011-2023
# Note: companies before 2011 left unchanged
dc = pd.read_excel('PolicyData/EntityListUSA/FedRegisterDates2011-2023.xlsx','Table_cleaned') # dc short for date check

# standardize date




## Clean date
# date = parse(str(df['Effective Date']))
# df['Effective Date'] = date.strftime("%Y-%m-%d")


## Drop duplicates
df = df.drop_duplicates()
df = df.reset_index(drop=True)

## Save to a new csv file
file_cleaned = file.replace('.csv','_cleaned.csv')
df.to_csv(f"PolicyData/EntityListUSA/{file_cleaned}")