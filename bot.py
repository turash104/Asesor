# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount


import pandas as pd
from collections import defaultdict
from collections import OrderedDict
import matplotlib.pyplot as plt
import random
import re
import ast
'''
df_family=pd.read_excel("p_0_family.xlsx")
df_medication=pd.read_excel("p_0_medication.xlsx")
df_history=pd.read_excel("p_0_history.xlsx")
df_allergy=pd.read_excel("p_0_allergy.xlsx")
df_ques=pd.read_excel("questions.xlsx")
df_ques=df_ques[["id", "text"]]

ques_list=[]
ques_list.append("Greetings!!")
for i, row in df_ques.iterrows():
    ques_list.append(row["text"])

past_medications=df_medication["medication"].tolist()
past_history=df_history["problem"].tolist()
past_allergy=df_allergy["allergy"].tolist()

#print(past_medications)
medic=" "
if len(past_medications)==1:
    medic=past_medications[-1]
elif len(past_medications)==2:
    medic+=past_medications[0]+" and "+past_medications[-1]
else:
    part1=past_medications[:-1]
    medic=", ".join(part1)
    medic+=", and "+past_medications[-1]

#print(past_history)
history=" "
if len(past_history)==1:
    history=past_history[-1]
elif len(past_history)==2:
    history+=past_history[0]+" and "+past_history[-1]
else:
    part1=past_history[:-1]
    history=", ".join(part1)
    history+=", and "+past_history[-1]

#print(past_allergy)
allergy=" "
if len(past_allergy)==1:
    allergy=past_allergy[-1]
elif len(past_allergy)==2:
    allergy+=past_allergy[0]+" and "+past_allergy[-1]
else:
    part1=past_allergy[:-1]
    allergy=", ".join(part1)
    allergy+=", and "+past_allergy[-1]

last_ques=18
current_ques=1


while(current_ques!=last_ques):
    next_ques=current_ques
    if current_ques==1:
        ans=input(ques_list[current_ques])
        if "new" in ans: next_ques=2
        elif "follow" in ans: next_ques=4
    elif current_ques==3:
        ans=input(ques_list[current_ques])
        next_ques=8
    elif current_ques==7:
        prompt=ques_list[current_ques].replace("placeholder", medic)
        ans=input(prompt)
        next_ques=8
    elif current_ques==8:
        prompt=ques_list[current_ques].replace("placeholder", history)
        ans=input(prompt)
        if "yes" in ans: next_ques=9
        elif "no" in ans: next_ques=10
    elif current_ques==10:
        prompt=ques_list[current_ques].replace("placeholder", allergy)
        ans=input(prompt)
        if "yes" in ans: next_ques=11
        elif "no" in ans: next_ques=16
    elif current_ques==11:
        ans=input(ques_list[current_ques])
        next_ques=16
    else:
        ans=input(ques_list[current_ques])
        next_ques=current_ques+1
    current_ques=next_ques
'''

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
    def __init__(self):
        self.cur_q_id=0
        self.prev_q_id=-1
        self.df_family = pd.read_excel("p_0_family.xlsx")
        self.df_medication = pd.read_excel("p_0_medication.xlsx")
        self.df_history = pd.read_excel("p_0_history.xlsx")
        self.df_allergy = pd.read_excel("p_0_allergy.xlsx")
        self.df_ques = pd.read_excel("questions.xlsx")
        self.df_ques = self.df_ques[["id", "text"]]

        self.ques_list = []
        self.ques_list.append("Greetings!!")
        for i, row in self.df_ques.iterrows():
            self.ques_list.append(row["text"])

        self.past_medications = self.df_medication["medication"].tolist()
        self.past_history = self.df_history["problem"].tolist()
        self.past_allergy = self.df_allergy["allergy"].tolist()

        #print(past_medications)

        self.medic = " "
        if len(self.past_medications) == 1:
            self.medic = self.past_medications[-1]
        elif len(self.past_medications) == 2:
            self.medic += self.past_medications[0] + " and " + self.past_medications[-1]
        else:
            part1 = self.past_medications[:-1]
            self.medic = ", ".join(part1)
            self.medic += ", and " + self.past_medications[-1]

        #print(past_history)

        self.history = " "
        if len(self.past_history) == 1:
            self.history = self.past_history[-1]
        elif len(self.past_history) == 2:
            self.history += self.past_history[0] + " and " + self.past_history[-1]
        else:
            part1 = self.past_history[:-1]
            self.history = ", ".join(part1)
            self.history += ", and " + self.past_history[-1]

        #print(past_allergy)
        self.allergy = " "
        if len(self.past_allergy) == 1:
            self.allergy = past_allergy[-1]
        elif len(self.past_allergy) == 2:
            self.allergy += self.past_allergy[0] + " and " + self.past_allergy[-1]
        else:
            part1 = self.past_allergy[:-1]
            self.allergy = ", ".join(part1)
            self.allergy += ", and " + self.past_allergy[-1]

        self.cur_q_id=1

    async def on_message_activity(self, turn_context: TurnContext):
        #await turn_context.send_activity(f"You said '{ turn_context.activity.text }'")

        if self.prev_q_id == 0:
            self.cur_q_id = 1

        elif self.prev_q_id == 1:
            if "new" in str(turn_context.activity.text):
                self.cur_q_id = 2
            else:
                self.cur_q_id = 4

        elif self.prev_q_id == 3:
            self.cur_q_id = 8

        elif self.prev_q_id == 8:
            if "yes" in str(turn_context.activity.text):
                self.cur_q_id = 9
            else:
                self.cur_q_id = 10

        elif self.prev_q_id == 10:
            if "yes" in str(turn_context.activity.text):
                self.cur_q_id = 11
            else:
                self.cur_q_id = 16

        elif self.prev_q_id == 11:
            self.cur_q_id = 16

        else: self.cur_q_id = self.prev_q_id + 1

        ques = self.ques_list[self.cur_q_id]
        if self.cur_q_id==7: ques = ques.replace("placeholder", self.medic)
        elif self.cur_q_id==8: ques = ques.replace("placeholder", self.history)
        elif self.cur_q_id == 10: ques = ques.replace("placeholder", self.allergy)
        await turn_context.send_activity(ques)
        self.prev_q_id = self.cur_q_id


    async def on_members_added_activity(self, members_added: ChannelAccount, turn_context: TurnContext):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")
