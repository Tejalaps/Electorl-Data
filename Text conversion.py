import os
import PyPDF2
import re
import pandas as pd
import numpy as np
import fitz

directory = r'C:\Users\AUSULTE\Downloads\e'

rows = []
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        
        with open(os.path.join(directory, filename),'r') as src_file:
            text_data = src_file.read()
        name_matches = re.findall(r'Name:\s([A-Z\s]+)\s', text_data)
        father_matches = re.findall(r"(Father|Husband|Mother)'s Name\s:\s([A-Z\s]+)\s",text_data)
        

        for i, name in enumerate(name_matches):
            name_parts = name.strip().split()
            if len(name_parts)>=2:
                full_name = ' '.join(name_parts)
            else:
                full_name = name.strip()
#             Relationship
            father_name = father_matches[i][0].strip()   
            father_parts = father_name.split()
            fathers_part = father_matches[i][0].strip().split()

            if len(father_parts)>=2:
                full_father_relation_name = ' '.join(father_parts[:2])
                full_father_name = ' '.join(father_part[:2])
            else:
                full_father_relation_name = father_name
                full_father_name = father_matches[i][1].strip()

       
            row= {
                'Name': full_name,
                "Relationship": full_father_relation_name,
                "Father/Husband/Mother Name": full_father_name
            }
            rows.append(row)
df = pd.DataFrame(rows)
df.head(6)           
