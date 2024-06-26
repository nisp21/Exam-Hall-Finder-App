import streamlit as st    
from PyPDF2 import PdfReader
import os
import glob

st.title("Seating Arrangement NIRMA UNIVERSITY")
uploaded_files = st.file_uploader("Choose one or more PDF files", accept_multiple_files=True)
roll_no = st.text_input('Enter your Roll_No:')
roll_no=roll_no.upper()

classes=['A-','B-','C-','D-','E-','N-']
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

    if len(uploaded_files):
        output.clear()
        for hehe in uploaded_files:
            reader = PdfReader(hehe)
            number_of_pages = len(reader.pages)

            for nisarg in range(number_of_pages):
                page = reader.pages[nisarg]
                text = page.extract_text()
                

                if text.find(roll_no)==-1:
                        continue
                
                Time=""
                for i in range(text.find("Time"),text.find("\n",text.find("Time"))):
                    Time= Time+text[i] 
                
                Date=""
                for i in range(text.find("Date"),text.find("T",text.find("Date"))):
                    Date= Date+text[i] 

                index_of_class=-1
                x=0
                while(1):
                    t=x
                    for i in range(len(classes)):
                        if text.find(classes[i],x)!=-1:
                            temp=text.find(classes[i],x)
                            if temp>text.find(roll_no):
                                break
                            index_of_class=temp
                            x=text.find(classes[i],x)
                            x=x+1
                            break
                    if t==x:
                        break
                
                if(index_of_class!=-1):
                    class_name=text[index_of_class:text.find(" ",index_of_class)]
                    if len(class_name)>5 and class_name[5] not in ['A','B','C','D']:
                        class_name=class_name[0:5]
                    else:
                        class_name=class_name[0:6]

                    output.append([roll_no,Date[0:find_last_occurrence(Date,'202')+4],class_name,Time[0:(find_third_occurrence(Time,"m")+1)]])
                    
        output.sort()
        (output)

    else:
        output.clear()
        for hehe in pdf_files:
            reader = PdfReader(hehe)
            number_of_pages = len(reader.pages)

            for nisarg in range(number_of_pages):
                page = reader.pages[nisarg]
                text = page.extract_text()
                

                if text.find(roll_no)==-1:
                        continue
                
                Time=""
                for i in range(text.find("Time"),text.find("\n",text.find("Time"))):
                    Time= Time+text[i] 
                
                Date=""
                for i in range(text.find("Date"),text.find("T",text.find("Date"))):
                    Date= Date+text[i] 

                index_of_class=-1
                x=0
                while(1):
                    t=x
                    for i in range(len(classes)):
                        if text.find(classes[i],x)!=-1:
                            temp=text.find(classes[i],x)
                            if temp>text.find(roll_no):
                                break
                            index_of_class=temp
                            x=text.find(classes[i],x)
                            x=x+1
                            break
                    if t==x:
                        break
                
                if(index_of_class!=-1):
                    class_name=text[index_of_class:text.find(" ",index_of_class)]
                    if len(class_name)>5 and class_name[5] not in ['A','B','C','D']:
                        class_name=class_name[0:5]
                    else:
                        class_name=class_name[0:6]

                    output.append([roll_no,Date[0:find_last_occurrence(Date,'202')+4],class_name,Time[0:(find_third_occurrence(Time,"m")+1)]])
        output.sort()
        output

st.text("NOTE : This might contains some mistake do check if output\nis less than the no_of_papers you are appearing")
st.text("Made by Nisarg Patel (21BCE211)")
