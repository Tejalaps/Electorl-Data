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
        name_matches = re.findall(r'Name:\s(.*?)\s',text_data)
        father_matches = re.findall(r"Father's Name\s:\s(.*?)\s",text_data)
        
        names = []
        fathers = []
        for i in range(len(name_matches)):
            names.append(name_matches[i])
            if i<len(father_matches):
                fathers.append(father_matches[i])
        
        for i, name in enumerate(names):
            row= {
                'Name': name.strip(),
                "Father\'s Name": fathers[i].strip() if i<len(fathers) else ''
            }
            rows.append(row)
df = pd.DataFrame(rows)
df.head(6)           
