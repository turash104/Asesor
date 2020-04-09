import pandas as pd
from collections import defaultdict
from collections import OrderedDict
import matplotlib.pyplot as plt
import random
import re
import ast
from nltk.corpus import wordnet as wn
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm



nlp = spacy.load("en")
print(nlp)

df_medications=pd.read_excel("sample_medication.xlsx")
medication_list=df_medications["text"].tolist()

for i in range(len(medication_list)):
    u=medication_list[i].strip()
    doc = nlp(u)
    dosages=[]
    timings=[]
    medications=[]
    purposes=[]

    dosage_indicators=["every", "each", "per", "once", "twice", "thrice", "times"]
    for ent in doc.ents:
        #print(ent.text, ent.label_)
        if ent.label_ == 'DATE':
            tex=ent.text.lower()
            if any(sub in tex for sub in dosage_indicators): dosages.append(tex)
            else: timings.append(tex)

    for chunk in doc.noun_chunks:
        #print("text: " + chunk.text)
        #print("label: " + chunk.label_)
        #print("root: " + chunk.root.text)
        if chunk.root.text == 'DATE':
            tex=chunk.text.lower()
            if any(sub in tex for sub in dosage_indicators): dosages.append(tex)
            else: timings.append(tex)
    
    
    parts=u.split()
    possible=["every", "once", "twice", "thrice"]
    for index, part in enumerate(parts):
        if (part=="times" or part=="time") and index>0:
            new_dosage=parts[index-1]+" "+parts[index]
            possible.append(new_dosage)

    u=u.lower() 
    possible_prefix="|".join(possible)
    possible_prefix="("+possible_prefix+")"
    m = re.findall(possible_prefix+'(.*?)(\\.|day|week|month|year)', u)
    
    if m!=None:
        for m_elem in m:
            t=m_elem[0]+m_elem[1]+m_elem[2]
            dosages.append(t)
    dosages=list(set(dosages))

    m = re.findall('(take|taking|took|taken|takes|taken)(.*?)(\\.|for|since)', u)
    
    if m!=None:
        for m_elem in m:
            t=m_elem[1]
            medications.append(t)
    medications=list(set(medications))
    
    m = re.findall('(take|taking|took|taken|takes|taken|use|using|used|uses|)(.*?)(for)(.+?)(\\.)', u)
    
    if m!=None:
        for m_elem in m:
            t=m_elem[3]
            purposes.append(t)
    purposes=list(set(purposes))

    print("response: ")
    print(doc)
    print("medications: ")
    print(medications)
    print("purpose: ")
    print(purposes)
    print("timing: ")
    print(timings)
    print("dosages: ")
    print(dosages)
    
    
        
            

