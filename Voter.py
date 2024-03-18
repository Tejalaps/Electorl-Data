import os
import PyPDF2
import re
import pandas as pd
import numpy as np

directory = r'C:\Users\AUSULTE\Downloads\Electoral_roll'

for filename in os.listdir(directory):
    if filename.endswith(".pdf"):
        src_file = open(os.path.join(directory, filename),'rb')
        pdfreader = PyPDF2.PdfFileReader(src_file)
        num_pg = pdfreader.getNumPages()

        start_pno = 2
        end_pno = num_pg-1
        
        for pg in range(start_pno,end_pno):
            pageob = pdfreader.getPage(pg)
            try:
                dest_file = open('pdf_content.txt','a')
            except FileNotFoundError:
                dest_file = open('pdf_content.txt','w')
#             print(pageob.extractText())
            dest_file.write(pageob.extractText())
            dest_file.close()

        src_file.close()

out_file = open('pdf_line_content.txt','w')
new_file = open('pdf_content.txt','rb')

s = new_file.read()
strn = re.split(' No',str(s))
out_file.write('\n'.join(strn))

new_file.close()
out_file.close()

out_fl = open('pdf_line_content.txt','r')

row = []

for eachline in out_fl.readlines():
    try:
        h_no = re.findall(r'\s:\s(.*?)Gender',eachline)
        if h_no:
            h_no= h_no[0].replace('\\r\\n','')
        else:
            h_no=""
        gender = re.findall(r'.Gender\s:\s(.*?)Age',eachline)
    #     name = re.findall(r'Name\s:\s(.*?)\s*',eachline)
        name = eachline.split("Name : ")[1].split(" ")[0].strip()
#         age = re.findall(r'[A-Z]*\s\s(\d\d)\s.\w',eachline)
#         f_name = re.findall(r'\sName\s:\s(.*?)\s\s\d\d',eachline)
        f_name_index = eachline.find("Father's Name : ")
    
        if f_name_index != -1:
            f_name = eachline[f_name_index+len("Father's Name : "):].split(" ")[0].strip()
        else:
            h_name_index = eachline.find("Husband's Name : ")
            if h_name_index != -1:
                f_name = eachline[h_name_index +len("Husband's Name : "):].split(" ")[0].strip()
            else:
                f_name=""
                
        age_index = eachline.find(f_name)
        if age_index != -1:
            age = re.findall(r'\d+',eachline[age_index+len(f_name):])[0]
        else:
            age =""
        print("Line:",eachline)
        print("HNO:", h_no)
        print("Gen:", gender)
        print("Name:",name)
        print("Age:",age)
        print("F/h Name",f_name)
        row.append((h_no,gender,name,age,f_name))
    except IndexError as e:
        print("Error:",e)
        print("Line:",eachline)

out_fl.close()
os.remove('pdf_content.txt')
os.remove('pdf_line_content.txt')

df = pd.DataFrame(row, columns = ['House No', 'Gender', 'Name', 'Age',
                                  'Father\'s/Husband\'s Name'])

for colmn in df.columns:
    df[colmn] = df[colmn].apply(lambda i: ''.join(i)) 

df.replace('', np.nan, inplace=True)
df.dropna(how = 'all', inplace=True)
df.head(10)
# writer = pd.ExcelWriter('output.xlsx')
# df.to_excel(writer,'Content')

# writer.close()
