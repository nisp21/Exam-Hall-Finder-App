import streamlit as st    
from PyPDF2 import PdfReader
import os
import glob
import re
import pandas as pd

st.title("Seating Arrangement NIRMA UNIVERSITY")
st.text("7th sem students can skip file uploading part")
uploaded_files = st.file_uploader("Choose one or more PDF files", accept_multiple_files=True)
roll_no = st.text_input('Enter your Roll_No:')
roll_no=roll_no.upper()

# classes=['p-','P-','A-','B-','C-','D-','E-','N-']
output=[]

def find_third_occurrence(lst, element):
    occurrence_count = 0
    
    for index, item in enumerate(lst):
        if item == element:
            occurrence_count += 1
            if occurrence_count == 3:
                return index
    
    return -1
 
def find_last_occurrence(s, substring):
    last_index = -1
    index = 0
    
    while True:
        index = s.find(substring, index)
        if index == -1:
            return last_index
        last_index = index
        index += 1


folder_path = './ocr'
pdf_files = glob.glob(os.path.join(folder_path, '*.pdf'))
cnt=0


if st.button("Get Info"):
    flag = True
    if len(roll_no)!=8: flag = False
    if not roll_no[:2].isdigit(): flag = False
    if not roll_no[2:5].isalpha(): flag = False
    if not roll_no[5:].isdigit(): flag = False
    if flag:
        if len(uploaded_files):
            pdf_files=uploaded_files
        output.clear()
        output.append(["Date","Room","Time"])
        for hehe in pdf_files:
            reader = PdfReader(hehe)
            number_of_pages = len(reader.pages)

            for nisarg in range(number_of_pages):
                page = reader.pages[nisarg]
                text = page.extract_text()


                if text.find(roll_no)==-1:
                        continue

                Time=""
                regex = r'(\d{1,2}\.\d{2} (?:am|pm) to \d{1,2}\.\d{2} (?:am|pm))'
                res = re.findall(regex, text)
                Time = ', '.join(res)

                Date=""
                for i in range(text.find("Date"),text.find("T",text.find("Date"))):
                    Date= Date+text[i] 

                index_of_class=-1
                index_of_class=text[0:text.find(roll_no)].rfind('-')
                index_of_class=index_of_class-1

                if(index_of_class!=-2):
                    class_name=text[index_of_class:text.find(" ",index_of_class)]
                    if len(class_name)>5 and class_name[5] not in ['A','B','C','D']:
                        class_name=class_name[0:5]
                    else:
                        class_name=class_name[0:6]

                    output.append([Date[7:find_last_occurrence(Date,'202')+4],class_name,Time])

        if len(output) == 1:
            st.text("Roll Number not Found")
        else:
            output[1:len(output)] = sorted(output[1:len(output)])
            df=pd.DataFrame(output)
            st.markdown(f"### {roll_no}'s Seating Arrangement")
            styled_df = df.style.apply(lambda x: ['font-weight: bold;' if x.name == 0 else '' for _ in x], axis=1)   
            html = styled_df.hide(axis="index").hide(axis="columns").to_html()
            st.write(html, unsafe_allow_html=True)

    else:
        st.text("Invalid Roll Number Format")

st.text("Made by Nisarg Patel (21BCE211)")

