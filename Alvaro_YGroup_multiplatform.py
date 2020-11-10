# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 19:45:05 2020

@author: agum
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 12:45:04 2020

@author: agum
"""

# LIBRARIES REQUIRED
import os
import timeit
import numpy as np
import csv
import matplotlib.pyplot as plt
from collections import Counter

# Get Start Time
start = timeit.default_timer()

file = 'C:/Users/TRAGUM/Documents/AGUM/New/YGroup/vgsales-12-4-2019.csv/vgsales-12-4-2019.csv'

# List with raw data read directly from file
mylist_raw = []
# List to store the different categories in file
mylist_cat = []

# Multi-platform analysis variables initialization
mylist_mp = []
n_games_mp = 0


# Index declarations
iRank = 0
iName = 1
iBsName = 2
iGenre = 3
iRating = 4
iPlatform = 5
iPublisher = 6
iDeveloper = 7
iVGScore = 8
iCriticScore = 9
iUserScore = 10
iShipped = 11
iGlobSales = 12
iNASales = 13
iPALSales = 14
iJPSales = 15
iOthSales = 16
iYear = 17
iLastUpd = 18
iUrl = 19
iStatus = 20
iVgScore2 = 21
iImgUrl = 22

# Open file and read it line by line
with open(file, 'r', encoding="utf-8") as file:
    csv_reader = csv.reader(file, delimiter=',')
    for row in csv_reader:
        if (row[iName] == 'Name'):
#           Only for first row            
            mylist_cat.append(row)
        else:
#           Filter out games with no information on sales or launching year
            if (row[iShipped] != '' or row[iGlobSales] != '' and (row[iYear] != '')):
                mylist_raw.append(row)
 
# Multi-platform analysis
zipped = zip(*mylist_raw)
mylist_col = list(zipped)
mydict_names = dict(Counter(mylist_col[iName]))
for key, value in mydict_names.items():
    if value != 1:
        n_games_mp = n_games_mp + value
    tmp_list = [key, value]
    mylist_mp.append(tmp_list)



# How many games have been published for different platforms?
# First, create a temporary variable from the raw one
mylist_tmp_raw = mylist_raw
mylist_mp = []
mylist_mp_sales = []
n_games_sp = 0
for i in range(len(mylist_tmp_raw)):
    sales = 0
    if mylist_tmp_raw[i][iRank] != '':
        name = mylist_tmp_raw[i][iName]
        flag = False
        mylist_mp_one = []
        count = -1
        if mylist_tmp_raw[i][iShipped] != '':
            sales = float(mylist_tmp_raw[i][iShipped]) + sales
        elif mylist_tmp_raw[i][iGlobSales] != '':
            sales = float(mylist_tmp_raw[i][iGlobSales]) + sales
        for j in range(i+1, len(mylist_tmp_raw)):
            if name == mylist_tmp_raw[j][iName]:
                count = count + 1
                if count == 0:
                    mylist_mp_one.append(name)
                    mylist_mp_one.append(mylist_tmp_raw[i][iPlatform])
                flag = True
                mylist_tmp_raw[j][iRank] = ''
                mylist_mp_one.append(mylist_tmp_raw[j][iPlatform])
                if mylist_tmp_raw[j][iShipped] != '':
                    sales = float(mylist_tmp_raw[j][iShipped]) + sales
                elif mylist_tmp_raw[j][iGlobSales] != '':
                    sales = float(mylist_tmp_raw[j][iGlobSales]) + sales
        if flag:
            mylist_mp.append(mylist_mp_one)
            mylist_mp_sales.append(sales)
        else:
            n_games_sp = n_games_sp + 1

n_games_mp = len(mylist_raw) - n_games_sp

# How many games have been published in both PS4/XOne?
n_games_mp_PSXBox = 0
n_games_mp_PSXBoxPC = 0
n_games_PC = 0
n_games_not_PSXBox = 0
sales_mp_PSXBox = 0
sales_mp_PSXBoxPC = 0
for i in range(len(mylist_mp)):
    tmp_list = dict(zip(mylist_mp[i],range(len(mylist_mp[i]))))
    if (tmp_list.get('PS4') != None and tmp_list.get('XOne') != None):
        n_games_mp_PSXBox = n_games_mp_PSXBox + 1
        sales_mp_PSXBox = sales_mp_PSXBox + mylist_mp_sales[i]
    if (tmp_list.get('PS3') != None and tmp_list.get('X360') != None):
        n_games_mp_PSXBox = n_games_mp_PSXBox + 1
        sales_mp_PSXBox = sales_mp_PSXBox + mylist_mp_sales[i]
    if (tmp_list.get('PS2') != None and tmp_list.get('XB') != None):
        n_games_mp_PSXBox = n_games_mp_PSXBox + 1
        sales_mp_PSXBox = sales_mp_PSXBox + mylist_mp_sales[i]
    if (tmp_list.get('PS4') != None and tmp_list.get('XOne') != None and tmp_list.get('PC') != None):
        n_games_mp_PSXBoxPC = n_games_mp_PSXBoxPC + 1
        sales_mp_PSXBoxPC = sales_mp_PSXBoxPC + mylist_mp_sales[i]
    elif (tmp_list.get('PS4') != None and tmp_list.get('PC') != None):
        n_games_mp_PSXBoxPC = n_games_mp_PSXBoxPC + 1
        sales_mp_PSXBoxPC = sales_mp_PSXBoxPC + mylist_mp_sales[i]
    elif (tmp_list.get('XOne') != None and tmp_list.get('PC') != None):
        n_games_mp_PSXBoxPC = n_games_mp_PSXBoxPC + 1
        sales_mp_PSXBoxPC = sales_mp_PSXBoxPC + mylist_mp_sales[i]
    if (tmp_list.get('PS3') != None and tmp_list.get('X360') != None and tmp_list.get('PC') != None):
        n_games_mp_PSXBoxPC = n_games_mp_PSXBoxPC + 1
        sales_mp_PSXBoxPC = sales_mp_PSXBoxPC + mylist_mp_sales[i]
    elif (tmp_list.get('PS3') != None and tmp_list.get('PC') != None):
        n_games_mp_PSXBoxPC = n_games_mp_PSXBoxPC + 1
        sales_mp_PSXBoxPC = sales_mp_PSXBoxPC + mylist_mp_sales[i]
    elif (tmp_list.get('X360') != None and tmp_list.get('PC') != None):
        n_games_mp_PSXBoxPC = n_games_mp_PSXBoxPC + 1
        sales_mp_PSXBoxPC = sales_mp_PSXBoxPC + mylist_mp_sales[i]
    if (tmp_list.get('PS2') != None and tmp_list.get('XB') != None and tmp_list.get('PC') != None):
        n_games_mp_PSXBoxPC = n_games_mp_PSXBoxPC + 1
        sales_mp_PSXBoxPC = sales_mp_PSXBoxPC + mylist_mp_sales[i]
    elif (tmp_list.get('PS2') != None and tmp_list.get('PC') != None):
        n_games_mp_PSXBoxPC = n_games_mp_PSXBoxPC + 1
        sales_mp_PSXBoxPC = sales_mp_PSXBoxPC + mylist_mp_sales[i]
    elif (tmp_list.get('XB') != None and tmp_list.get('PC') != None):
        n_games_mp_PSXBoxPC = n_games_mp_PSXBoxPC + 1
        sales_mp_PSXBoxPC = sales_mp_PSXBoxPC + mylist_mp_sales[i]


# Multi-platform
plt.title('Multi-platform games published (1990-2019)')
height = [len(mylist_mp), n_games_mp_PSXBox, n_games_mp_PSXBoxPC]
bars = ('Total', 'PlayStation & XBox', 'PlayStation & XBox & PC')
 
y_pos = [0,2,4]
plt.ylabel('Number of published games')
plt.bar(y_pos, height, color=['red', 'blue', 'green'],  edgecolor='black')
plt.xticks(y_pos, bars)

plt.savefig(os.getcwd()+'\\multiplatform_games.png', dpi=1000)
plt.show()

# Multi-platform
plt.title('Multi-platform games sales (1990-2019)')
height = [sum(mylist_mp_sales), sales_mp_PSXBox, sales_mp_PSXBoxPC]
bars = ('Total', 'PlayStation & XBox', 'PlayStation & XBox & PC')
 
y_pos = [0,2,4]
plt.ylabel('Copies sold (in million)')
plt.bar(y_pos, height, color=['red', 'blue', 'green'],  edgecolor='black')
plt.xticks(y_pos, bars)

plt.savefig(os.getcwd()+'\\multiplatform_sales.png', dpi=1000)
plt.show()