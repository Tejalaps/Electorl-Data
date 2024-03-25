import os
import PyPDF2
import re
import pandas as pd
import numpy as np
import fitz

directory = r'C:\Users\AUSULTE\Downloads\e'

rows = []
current_assembly = None
current_part_number = None
section_name = None
current_constituency = None
current_pincode = None
current_village = None

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        
        with open(os.path.join(directory, filename),'r') as src_file:
            text_data = src_file.read()
        
    
        name_matches = re.findall(r'Name\s*:\s*([A-Za-z\s]+)\s', text_data,re.IGNORECASE)
#         name_matches = re.findall(r'Name\s*:\s*([A-Za-z\s]+)\s(?=Father\'s Name|House Number|Age|Gender)', text_data)
        father_matches = re.findall(r"(Fathers|Father's|Husband's|Mother's|Husbands|Mothers)\s+Name\s*:\s*([A-Za-z\s]+)\s",text_data,re.IGNORECASE)
#         house_matches = re.findall(r'House Number:\s(\S+)\s',text_data)
        house_matches = re.findall(r'House\s*(?:Number|No\.)\s*:\s*(\S+)\s',text_data,re.IGNORECASE)
        age_matches = re.findall(r'Age\s*:\s*(\d+)\s', text_data,re.IGNORECASE)
        gender_matches = re.findall(r'Gender\s*:\s*([A-Z]+)\s',text_data,re.IGNORECASE)
        assembly_match = re.search(r'Assembly Constituency No and Name : (.+?)\sPart', text_data,re.IGNORECASE)
        part_number_matches = re.findall(r'Part\s*(?:Number|No\.)\s*:\s*(\d+)', text_data,re.IGNORECASE)
        section_matches = re.findall(r'Section No and Name\s*(?::\s*)?(.+)\s', text_data,re.IGNORECASE)
        Constituency_matches = re.findall(r'Constituency is located\s*:\s*(.*(?:\n\S.*))', text_data)
        pincode_matches = re.findall(r'Pin Code\s(.+)\s', text_data, re.IGNORECASE)
        village_matches = re.findall(r"Main\s+Town(?:\/|\sor\s)Village\s*:\s*(.+)",text_data,re.IGNORECASE)
#         ps_matches = re.findall(r"\b(?:Male/Female/General)\b[\s\n]*\n*(\S+)\s*",text_data)
        ps_matches = re.findall(r"\((?:Male/Female/General)\)[\s\n]*\n*(.+)",text_data)



        if section_matches:
            section_name = section_matches[0]

        if part_number_matches:
            current_part_number = part_number_matches[0]

        if assembly_match:
            current_assembly = assembly_match.group(1)
        if Constituency_matches:
            current_constituency = Constituency_matches[0]
        if pincode_matches:
            current_pincode = pincode_matches[0]
        if village_matches:
            current_village = village_matches[0]
        if ps_matches:
            current_ps = ps_matches[0]
            
        for i, name in enumerate(name_matches):
            name_parts = name.strip().split()
            if len(name_parts)>=2:
                full_name = ' '.join(name_parts)
            else:
                full_name = name.strip()
            unwanted_words = ['Name', 'Husbands', 'Fathers', 'Mothers','House Number']
            if i == 0:
                full_name = ' '.join([word for word in name_parts if word not in unwanted_words])
                
#             Relationship
            if i < len(father_matches):
                father_name = father_matches[i][1].strip()   
                father_parts = father_name.split()
                full_father_name = ' '.join(father_parts[:2]) if len(father_parts) >= 2 else father_name
                full_father_relation_name = father_matches[i][0].strip()
            else:
                full_father_name = None
                full_father_relation_name = None
                

#             if len(father_parts)>=2:
#                 full_father_relation_name = ' '.join(father_parts[:2])
#                 full_father_name = ' '.join(father_parts[:2])
#             else:
#                 full_father_relation_name = father_name
#                 full_father_name = father_matches[i][1].strip()
#             Father/Husband/Mother Name
#             House number
            try:
                house_number = house_matches[i]
            except IndexError:
                house_number = None
            try:
                age = age_matches[i]
            except IndexError:
                age = None
            try:
                gender = gender_matches[i]
            except IndexError:
                gender = None
            currrent_ps = None
            if ps_matches and i <len(ps_matches):
                current_ps = ps_matches[i]
            
                
            row= {
                'Name': full_name if not any(full_name in f for f in father_matches) else None,
#                 "Name": full_name if not any(full_name == f[1] for f in father_matches) else None,
                "Father/Husband/Mother Name": full_father_name if full_father_relation_name is not None else None,
                "Relationship": full_father_relation_name,
                "House No": house_number,
                "Age": age,
                "Gender": gender,
                "Assembly":current_assembly,
                "Part number": current_part_number,
                "Section no and name":section_name,
                "Constituency is located":current_constituency,
                "Pin Code":current_pincode,
                "Village":current_village,
                "Polling Station Name":current_ps
                
            }
            rows.append(row)
df = pd.DataFrame(rows)
# df = df.dropna(subset=['Relationship', 'Father/Husband/Mother Name'], how='all')

# Reset index after dropping rows
df.reset_index(drop=True, inplace=True)
# df.head(10)           
writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer,'Voter List')
writer.close()
