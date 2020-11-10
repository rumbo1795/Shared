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

# List with the different platforms (consoles) found in file
mylist_platform = []
# List with the different genres of games found in file
mylist_genre = []
# List with the different ESRB ratings of games found in file
mylist_rating = []
# List with the different Publisher of games found in file
mylist_publisher = []

# Population per region (in million)
population_NA = 579
population_PAL = 747
population_JP = 127

# Time range of market size study
start_year = 1990
end_year = 2020
mylist_time = np.linspace(start_year, end_year, (end_year - start_year + 1))

# List that contains home consoles
mylist_homeplatforms = ['PS','PS2', 'PS3', 'PS4', 'XB', 'X360', 'XOne', 'PC', 'Wii']
i_index_homeplatforms = np.zeros(len(mylist_homeplatforms))
tmp_sales_platform_home = np.zeros((len(mylist_homeplatforms), len(mylist_time)))
sales_platform_home = np.zeros(len(mylist_time))
# List that contains portable consoles
mylist_portplatforms = ['PSP','PSV', 'DS', '3DS', 'NS', 'GB', 'GBA', 'WiiU']
i_index_portplatforms = np.zeros(len(mylist_portplatforms))
tmp_sales_platform_port = np.zeros((len(mylist_homeplatforms), len(mylist_time)))
sales_platform_port = np.zeros(len(mylist_time))

# Multi-platform analysis variables initialization
mylist_mp = []
n_games_mp = 0

# Different sales categories(4) : Global Sales (or Total Shipped), NA, PAL, JP, Other
nSalesGeo = 5
# List of games (name) that have been published in more than one platform
mylist_mp_name = []

mylistplatform = []
mylistPlatformPS = [10, 7, 8]
mylistPlatformXB = [18, 5, 16]


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

# Order the information per column as well
zipped = zip(*mylist_raw)
mylist_col = list(zipped)
                
# 1. Obtain the different platforms
for i in range(len(mylist_raw)):
    platform = mylist_raw[i][iPlatform]
    flag = True
    if len(mylist_platform) != 0:
        for j in range(len(mylist_platform)):
            if platform == mylist_platform[j]:
                flag = False
                break
        if flag:
            mylist_platform.append(platform)
            if platform in mylist_homeplatforms:
                ind1 = mylist_homeplatforms.index(platform)
                ind2 = mylist_platform.index(platform)
                i_index_homeplatforms[ind1] = ind2
            elif platform in mylist_portplatforms:
                ind1 = mylist_portplatforms.index(platform)
                ind2 = mylist_platform.index(platform)
                i_index_portplatforms[ind1] = ind2                
    else:
        mylist_platform.append(platform)

# 1.1. Obtain the consoles with more sales per year
sales_platform = np.zeros((len(mylist_platform), len(mylist_time)))
#n_games_platform = np.zeros(len(mylist_platform), len(mylist_time))
for i in range(len(mylist_raw)):
    platform = mylist_raw[i][iPlatform]
    for j in range(len(mylist_platform)):
        if platform == mylist_platform[j]:
            if mylist_raw[i][iPlatform] == mylist_platform[j]:
                if float(mylist_raw[i][iYear]) >= mylist_time[0] and float(mylist_raw[i][iYear]) <= mylist_time[-1]:
                    iTime = int(float(mylist_raw[i][iYear]) - start_year)
                    if mylist_raw[i][iShipped] != '':
                        sales_platform[j][iTime] = float(mylist_raw[i][iShipped]) + sales_platform[j][iTime]
                    elif mylist_raw[i][iGlobSales] != '':
                        sales_platform[j][iTime] = float(mylist_raw[i][iGlobSales]) + sales_platform[j][iTime]
                        break
                else:
                    break
                
# Obtain sales per type of console over the years (home/portable)
# Home
for i in range(len(mylist_homeplatforms)):
    for j in range(len(mylist_time)):
        tmp_sales_platform_home[i][j] = sales_platform[int(i_index_homeplatforms[i])][j]
sales_platform_home[:] = [sum(x) for x in zip(*tmp_sales_platform_home)]

# Portable
for i in range(len(mylist_portplatforms)):
    for j in range(len(mylist_time)):
        tmp_sales_platform_port[i][j] = sales_platform[int(i_index_portplatforms[i])][j]
sales_platform_port[:] = [sum(x) for x in zip(*tmp_sales_platform_port)]

#############################GEOGRAPHY########################################
# Get sales per market per year
sales_years = np.zeros(len(mylist_time))
sales_years_NA = np.zeros(len(mylist_time))
sales_years_PAL = np.zeros(len(mylist_time))
sales_years_JP = np.zeros(len(mylist_time))
for i in range(len(mylist_raw)):
    if float(mylist_raw[i][iYear]) >= mylist_time[0] and float(mylist_raw[i][iYear]) <= mylist_time[-1]:
        iTime = int(float(mylist_raw[i][iYear]) - start_year)
        if mylist_raw[i][iShipped] != '':
            sales_years[iTime] = float(mylist_raw[i][iShipped]) + sales_years[iTime]
        elif mylist_raw[i][iGlobSales] != '':
            sales_years[iTime] = float(mylist_raw[i][iGlobSales]) + sales_years[iTime]
            if mylist_raw[i][iNASales] != '':
                sales_years_NA[iTime] = float(mylist_raw[i][iNASales]) + sales_years_NA[iTime]
            if mylist_raw[i][iPALSales] != '':
                sales_years_PAL[iTime] = float(mylist_raw[i][iPALSales]) + sales_years_PAL[iTime]
            if mylist_raw[i][iJPSales] != '':
                sales_years_JP[iTime] = float(mylist_raw[i][iJPSales]) + sales_years_JP[iTime]
                

#############################GENRE############################################
# Obtain the different genres
mydict_genre = dict(Counter(mylist_col[iGenre]))
for key, value in mydict_genre.items():
    tmp_list = [key, value]
    mylist_genre.append(tmp_list)

# Obtain sales per genre over the years worldwide and per region
sales_genre_years = np.zeros((len(mylist_genre), len(mylist_time)))
sales_genre_years_NA = np.zeros((len(mylist_genre), len(mylist_time)))
sales_genre_years_PAL = np.zeros((len(mylist_genre), len(mylist_time)))
sales_genre_years_JP = np.zeros((len(mylist_genre), len(mylist_time)))
for i in range(len(mylist_raw)):
    genre = mylist_raw[i][iGenre]
    for j in range(len(mylist_genre)):
        if genre == mylist_genre[j][0]:
            if mylist_raw[i][iGenre] == mylist_genre[j][0]:
                if float(mylist_raw[i][iYear]) >= mylist_time[0] and float(mylist_raw[i][iYear]) <= mylist_time[-1]:
                    iTime = int(float(mylist_raw[i][iYear]) - start_year)
                    if mylist_raw[i][iShipped] != '':
                        sales_genre_years[j][iTime] = float(mylist_raw[i][iShipped]) + sales_genre_years[j][iTime]
                    elif mylist_raw[i][iGlobSales] != '':
                        sales_genre_years[j][iTime] = float(mylist_raw[i][iGlobSales]) + sales_genre_years[j][iTime]
                        if mylist_raw[i][iNASales] != '':
                            sales_genre_years_NA[j][iTime] = float(mylist_raw[i][iNASales]) + sales_genre_years_NA[j][iTime]
                        if mylist_raw[i][iPALSales] != '':
                            sales_genre_years_PAL[j][iTime] = float(mylist_raw[i][iPALSales]) + sales_genre_years_PAL[j][iTime]
                        if mylist_raw[i][iJPSales] != '':
                            sales_genre_years_JP[j][iTime] = float(mylist_raw[i][iJPSales]) + sales_genre_years_JP[j][iTime]
                        break
                else:
                    break

# Get top 10 in sales of Shooter games
shooter = []
mylist_raw_tmp = mylist_raw
for i in range(10):
    sales_ref = 0
    for i in range(len(mylist_raw_tmp)):
        if mylist_raw_tmp[i][iGenre] == 'Shooter':
            if mylist_raw_tmp[i][iShipped] != '':
                if float(mylist_raw_tmp[i][iShipped]) > sales_ref:
                    sales_ref = float(mylist_raw_tmp[i][iShipped])
                    mylist_raw_tmp[i][iShipped] = '0'
                    index = i
                    name = mylist_raw_tmp[i][iName]
            elif mylist_raw_tmp[i][iGlobSales] != '':
                if float(mylist_raw_tmp[i][iGlobSales]) > sales_ref:
                    sales_ref = float(mylist_raw_tmp[i][iGlobSales])
                    mylist_raw_tmp[i][iGlobSales] = '0'
                    index = i
                    name = mylist_raw_tmp[i][iName]
    shooter.append(name)

# Get top 10 in sales of Action games
action = []
mylist_raw_tmp = mylist_raw
for i in range(10):
    sales_ref = 0
    for i in range(len(mylist_raw_tmp)):
        if mylist_raw_tmp[i][iGenre] == 'Action':
            if mylist_raw_tmp[i][iShipped] != '':
                if float(mylist_raw_tmp[i][iShipped]) > sales_ref:
                    sales_ref = float(mylist_raw_tmp[i][iShipped])
                    mylist_raw_tmp[i][iShipped] = '0'
                    index = i
                    name = mylist_raw_tmp[i][iName]
            elif mylist_raw_tmp[i][iGlobSales] != '':
                if float(mylist_raw_tmp[i][iGlobSales]) > sales_ref:
                    sales_ref = float(mylist_raw_tmp[i][iGlobSales])
                    mylist_raw_tmp[i][iGlobSales] = '0'
                    index = i
                    name = mylist_raw_tmp[i][iName]
    action.append(name)

# Get top 10 in sales of Sports games
sports = []
mylist_raw_tmp = mylist_raw
for i in range(10):
    sales_ref = 0
    for i in range(len(mylist_raw_tmp)):
        if mylist_raw_tmp[i][iGenre] == 'Sports':
            if mylist_raw_tmp[i][iShipped] != '':
                if float(mylist_raw_tmp[i][iShipped]) > sales_ref:
                    sales_ref = float(mylist_raw_tmp[i][iShipped])
                    mylist_raw_tmp[i][iShipped] = '0'
                    index = i
                    name = mylist_raw_tmp[i][iName]
            elif mylist_raw_tmp[i][iGlobSales] != '':
                if float(mylist_raw_tmp[i][iGlobSales]) > sales_ref:
                    sales_ref = float(mylist_raw_tmp[i][iGlobSales])
                    mylist_raw_tmp[i][iGlobSales] = '0'
                    index = i
                    name = mylist_raw_tmp[i][iName]
    sports.append(name)

# COD sales throughout the years
sales_cod_years = np.zeros(len(mylist_time))
n_games_cod = 0
name_reference = 'Call of Duty'
for i in range(len(mylist_raw)):
    name = mylist_raw[i][iName]
    if name[0:len(name_reference)] == name_reference:
        n_games_cod = n_games_cod + 1
        if float(mylist_raw[i][iYear]) >= mylist_time[0] and float(mylist_raw[i][iYear]) <= mylist_time[-1]:
            iTime = int(float(mylist_raw[i][iYear]) - start_year)
            if mylist_raw[i][iShipped] != '':
                sales_cod_years[iTime] = float(mylist_raw[i][iShipped]) + sales_cod_years[iTime]
            elif mylist_raw[i][iGlobSales] != '':
                sales_cod_years[iTime] = float(mylist_raw[i][iGlobSales]) + sales_cod_years[iTime]

# GTA sales throughout the years
sales_gta_years = np.zeros(len(mylist_time))
n_games_gta = 0
name_reference = 'Grand Theft Auto'
for i in range(len(mylist_raw)):
    name = mylist_raw[i][iName]
    if name[0:len(name_reference)] == name_reference:
        n_games_gta = n_games_gta + 1
        if float(mylist_raw[i][iYear]) >= mylist_time[0] and float(mylist_raw[i][iYear]) <= mylist_time[-1]:
            iTime = int(float(mylist_raw[i][iYear]) - start_year)
            if mylist_raw[i][iShipped] != '':
                sales_gta_years[iTime] = float(mylist_raw[i][iShipped]) + sales_gta_years[iTime]
            elif mylist_raw[i][iGlobSales] != '':
                sales_gta_years[iTime] = float(mylist_raw[i][iGlobSales]) + sales_gta_years[iTime]
                
# FIFA sales throughout the years
sales_fifa_years = np.zeros(len(mylist_time))
n_games_fifa = 0
name_reference = 'FIFA'
for i in range(len(mylist_raw)):
    name = mylist_raw[i][iName]
    if name[0:len(name_reference)] == name_reference:
        n_games_fifa = n_games_fifa + 1
        if float(mylist_raw[i][iYear]) >= mylist_time[0] and float(mylist_raw[i][iYear]) <= mylist_time[-1]:
            iTime = int(float(mylist_raw[i][iYear]) - start_year)
            if mylist_raw[i][iShipped] != '':
                sales_fifa_years[iTime] = float(mylist_raw[i][iShipped]) + sales_fifa_years[iTime]
            elif mylist_raw[i][iGlobSales] != '':
                sales_fifa_years[iTime] = float(mylist_raw[i][iGlobSales]) + sales_fifa_years[iTime]

# Percentage of Wii Sports & Wii Fit sales in action genre
sales_wiisf_years = np.zeros(len(mylist_time))
name_reference = 'Wii Sports'
name_reference2 = 'Wii Fit'
for i in range(len(mylist_raw)):
    name = mylist_raw[i][iName]
    if name[0:len(name_reference)] == name_reference or name[0:len(name_reference2)] == name_reference2:
        if float(mylist_raw[i][iYear]) >= mylist_time[0] and float(mylist_raw[i][iYear]) <= mylist_time[-1]:
            iTime = int(float(mylist_raw[i][iYear]) - start_year)
            if mylist_raw[i][iShipped] != '':
                sales_wiisf_years[iTime] = float(mylist_raw[i][iShipped]) + sales_wiisf_years[iTime]
            elif mylist_raw[i][iGlobSales] != '':
                sales_wiisf_years[iTime] = float(mylist_raw[i][iGlobSales]) + sales_wiisf_years[iTime]
    
    
################################ESRB Rating####################################
# Get different ratings and number
mydict_rating = dict(Counter(mylist_col[iRating]))
for key, value in mydict_rating.items():
    tmp_list = [key, value]
    mylist_rating.append(tmp_list)

# Get sales per rating per market per year
sales_rating_years = np.zeros((len(mylist_rating), len(mylist_time)))
sales_rating_years_NA = np.zeros((len(mylist_rating), len(mylist_time)))
sales_rating_years_PAL = np.zeros((len(mylist_rating), len(mylist_time)))
sales_rating_years_JP = np.zeros((len(mylist_rating), len(mylist_time)))
for i in range(len(mylist_raw)):
    rating = mylist_raw[i][iRating]
    for j in range(len(mylist_rating)):
        if rating == mylist_rating[j][0]:
            if mylist_raw[i][iRating] == mylist_rating[j][0]:
                if float(mylist_raw[i][iYear]) >= mylist_time[0] and float(mylist_raw[i][iYear]) <= mylist_time[-1]:
                    iTime = int(float(mylist_raw[i][iYear]) - start_year)
                    if mylist_raw[i][iShipped] != '':
                        sales_rating_years[j][iTime] = float(mylist_raw[i][iShipped]) + sales_rating_years[j][iTime]
                    elif mylist_raw[i][iGlobSales] != '':
                        sales_rating_years[j][iTime] = float(mylist_raw[i][iGlobSales]) + sales_rating_years[j][iTime]
                        if mylist_raw[i][iNASales] != '':
                            sales_rating_years_NA[j][iTime] = float(mylist_raw[i][iNASales]) + sales_rating_years_NA[j][iTime]
                        if mylist_raw[i][iPALSales] != '':
                            sales_rating_years_PAL[j][iTime] = float(mylist_raw[i][iPALSales]) + sales_rating_years_PAL[j][iTime]
                        if mylist_raw[i][iJPSales] != '':
                            sales_rating_years_JP[j][iTime] = float(mylist_raw[i][iJPSales]) + sales_rating_years_JP[j][iTime]
                        break
                else:
                    break

# Total sales per rating
sales_rating_tot_world = np.zeros(len(mylist_rating))
sales_rating_tot_NA = np.zeros(len(mylist_rating))
sales_rating_tot_PAL = np.zeros(len(mylist_rating))
sales_rating_tot_JP = np.zeros(len(mylist_rating))
for i in range(len(mylist_rating)):
    sales_rating_tot_world[i] = sum(sales_rating_years[i])
    sales_rating_tot_NA[i] = sum(sales_rating_years_NA[i])
    sales_rating_tot_PAL[i] = sum(sales_rating_years_PAL[i])
    sales_rating_tot_JP[i] = sum(sales_rating_years_JP[i])

# Find out which genres classify for each rating
mylist_ratingE_genre = []
mylist_ratingE10_genre = []
mylist_ratingT_genre = []
mylist_ratingM_genre = []

for i in range(len(mylist_raw)):
    rating = mylist_raw[i][iRating]
    if rating == 'E':
       mylist_ratingE_genre.append(mylist_raw[i][iGenre])
    elif rating == 'E10':
       mylist_ratingE10_genre.append(mylist_raw[i][iGenre]) 
    elif rating == 'T':
       mylist_ratingT_genre.append(mylist_raw[i][iGenre]) 
    elif rating == 'M':
       mylist_ratingM_genre.append(mylist_raw[i][iGenre])

mydict_ratingE_genre = dict(Counter(mylist_ratingE_genre))
mydict_ratingE10_genre = dict(Counter(mylist_ratingE10_genre))
mydict_ratingT_genre = dict(Counter(mylist_ratingT_genre))
mydict_ratingM_genre = dict(Counter(mylist_ratingM_genre))


###############################PUBLISHER######################################
# First, obtain the list of publishers in the file
mydict_publisher = dict(Counter(mylist_col[iPublisher]))
for key, value in mydict_publisher.items():
    tmp_list = [value, key]
    mylist_publisher.append(tmp_list)

mylist_publisher.sort(reverse = True)

# Analysis of top-5 publishers
n_top = 5
sales_publisher = np.zeros(n_top)
sales_publisher_NA = np.zeros(n_top)
sales_publisher_PAL = np.zeros(n_top)
sales_publisher_JP = np.zeros(n_top)

genre_publisher = [[] for i in range(n_top)]
platform_publisher = [[] for i in range(n_top)]

for i in range(len(mylist_raw)):
    publisher = mylist_raw[i][iPublisher]
    for j in range(n_top):
        if publisher == mylist_publisher[j][-1]:
            genre_publisher[j].append(mylist_raw[i][iGenre])
            platform_publisher[j].append(mylist_raw[i][iPlatform])
            if mylist_raw[i][iShipped] != '':
                sales_publisher[j] = float(mylist_raw[i][iShipped]) + sales_publisher[j]
            elif mylist_raw[i][iGlobSales] != '':
                sales_publisher[j] = float(mylist_raw[i][iGlobSales]) + sales_publisher[j]
                if mylist_raw[i][iNASales] != '':
                    sales_publisher_NA[j] = float(mylist_raw[i][iNASales]) + sales_publisher_NA[j]
                if mylist_raw[i][iPALSales] != '':
                    sales_publisher_PAL[j] = float(mylist_raw[i][iPALSales]) + sales_publisher_PAL[j]
                if mylist_raw[i][iJPSales] != '':
                    sales_publisher_JP[j] = float(mylist_raw[i][iJPSales]) + sales_publisher_JP[j]
                break
            
# Analyse Activision
for i in range(len(mylist_publisher)):
    if mylist_publisher[i][-1] == 'Activision':
        index_activision = i
        break

genre_activision = dict(Counter(genre_publisher[index_activision]))
platform_activision = dict(Counter(platform_publisher[index_activision]))

# Analyse Konami
for i in range(len(mylist_publisher)):
    if mylist_publisher[i][-1] == 'Konami':
        index_konami = i
        break

platform_konami = dict(Counter(platform_publisher[index_konami]))

# Analyse Nintendo
for i in range(len(mylist_publisher)):
    if mylist_publisher[i][-1] == 'Nintendo':
        index_nintendo = i
        break

platform_nintendo = dict(Counter(platform_publisher[index_nintendo]))



#############################PLOTS############################################

# Plot consoles sales per year (per type of console)
plt.figure()
plt.title('Sales evolution in time (Home vs Portable consoles)')
plt.plot(mylist_time, sales_platform_home, '-', label = 'Home: PS, XBox, PC, Wii')
plt.plot(mylist_time, sales_platform_port, '-', label = 'Portable: PS, NS, DS, GB, WiiU')

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()
plt.savefig(os.getcwd()+'\\home_portable_consoles.png', dpi=1000)
plt.show()

# Plot PlayStaion sales
plt.figure()
plt.title('Games copies sold vs launching year (PlayStation)')
for i in range(0, 4):
    plt.plot(mylist_time, sales_platform[int(i_index_homeplatforms[i])], '-', label = mylist_homeplatforms[i])

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()
plt.savefig(os.getcwd()+'\\playstation_study.png', dpi=1000)
plt.show()

# Plot XBox sales
plt.figure()
plt.title('Games copies sold vs launching year (XBox)')
for i in range(4, 7):
    plt.plot(mylist_time, sales_platform[int(i_index_homeplatforms[i])], '-', label = mylist_homeplatforms[i])

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()
plt.savefig(os.getcwd()+'\\xbox_study.png', dpi=1000)
plt.show()

# Plot PC sales
plt.figure()
plt.title('Games copies sold vs launching year (PC)')
i = 7
plt.plot(mylist_time, sales_platform[int(i_index_homeplatforms[i])], '-', label = mylist_homeplatforms[i])

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()
plt.savefig(os.getcwd()+'\\pc_study.png', dpi=1000)
plt.show()

# Plot Wii sales
plt.figure()
plt.title('Games copies sold vs launching year (Wii)')
i = 8
plt.plot(mylist_time, sales_platform[int(i_index_homeplatforms[i])], '-', label = mylist_homeplatforms[i], color = 'orange')

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()
plt.savefig(os.getcwd()+'\\wii_study.png', dpi=1000)
plt.show()

# 1.2. Plot consoles sales per year
plt.figure()
plt.title('Games copies sold vs launching year (per console)')
for i in range(len(mylist_homeplatforms)):
    plt.plot(mylist_time, sales_platform[int(i_index_homeplatforms[i])], '-', label = mylist_homeplatforms[i])

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()

plt.show()

################################################################################
# 1.2. Plot genre sales per year
sales_mean = np.mean(sum(sales_genre_years))
plt.figure()
plt.title('Games copies sold vs launching year (per genre)')
for i in range(len(mylist_genre)):
    if(sum(sales_genre_years[i])/sales_mean >= 1.5):
        plt.plot(mylist_time, sales_genre_years[i], '-', label = mylist_genre[i][0])

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()

plt.show()

# 1.2. Plot genre sales per year (NA)
sales_mean_NA = np.mean(sum(sales_genre_years_NA))
plt.figure()
plt.title('Games copies sold vs launching year per genre (NA)')
for i in range(len(mylist_genre)):
    if(sum(sales_genre_years_NA[i])/sales_mean_NA >= 2.0):
        plt.plot(mylist_time, sales_genre_years_NA[i], '-', label = mylist_genre[i][0])

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()
plt.savefig(os.getcwd()+'\\genre_study_NA.png', dpi=1000)
plt.show()

# 1.2. Plot genre sales per year (Europe)
sales_mean_PAL = np.mean(sum(sales_genre_years_PAL))
plt.figure()
plt.title('Games copies sold vs launching year per genre (Europe)')
for i in range(len(mylist_genre)):
    if(sum(sales_genre_years_PAL[i])/sales_mean_PAL >= 2.0):
        plt.plot(mylist_time, sales_genre_years_PAL[i], '-', label = mylist_genre[i][0])

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()
plt.savefig(os.getcwd()+'\\genre_study_PAL.png', dpi=1000)
plt.show()

# 1.2. Plot genre sales per year (Japan)
sales_mean_JP = np.mean(sum(sales_genre_years_JP))
plt.figure()
plt.title('Games copies sold vs launching year per genre (Japan)')
for i in range(len(mylist_genre)):
    if(sum(sales_genre_years_JP[i])/sales_mean_JP >= 2.0):
        plt.plot(mylist_time, sales_genre_years_JP[i], '-', label = mylist_genre[i][0])

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()
plt.savefig(os.getcwd()+'\\genre_study_JP.png', dpi=1000)
plt.show()

# Quesitos por rating
# Rating E
percentage = []
genre = []
misc_perc = 0
total_games_ratingE = mydict_rating.get('E')

for key, value in mydict_ratingE_genre.items():
    tmp_perc = value / total_games_ratingE * 100
    if tmp_perc > 5:
        percentage.append(tmp_perc)
        genre.append(key)
    else:
        misc_perc = misc_perc + tmp_perc

percentage.append(misc_perc)
genre.append('Rest')

m = max(percentage)
index = [i for i, j in enumerate(percentage) if j == m]
explode = [0] * len(percentage)
explode[index[0]] = 0.2

plt.pie(percentage, labels=genre, autopct='%1.1f%%', startangle=90, explode = explode)
plt.title('Games published in E (Everyone) rating category')
plt.savefig(os.getcwd()+'\\rating_pie_E.png', dpi=1000)
plt.show()

# Rating E10
percentage = []
genre = []
misc_perc = 0
total_games_ratingE10 = mydict_rating.get('E10')

for key, value in mydict_ratingE10_genre.items():
    tmp_perc = value / total_games_ratingE10 * 100
    if tmp_perc > 4:
        percentage.append(tmp_perc)
        genre.append(key)
    else:
        misc_perc = misc_perc + tmp_perc

percentage.append(misc_perc)
genre.append('Rest')

m = max(percentage)
index = [i for i, j in enumerate(percentage) if j == m]
explode = [0] * len(percentage)
explode[index[0]] = 0.2

plt.pie(percentage, labels=genre, autopct='%1.1f%%', startangle=90, explode = explode)
plt.title('Percentage of genre in E10 (Everyone+10) Rating Category')
plt.savefig(os.getcwd()+'\\rating_pie_E10.png', dpi=1000)
plt.show()

# Rating T
percentage = []
genre = []
misc_perc = 0
total_games_ratingT = mydict_rating.get('T')

for key, value in mydict_ratingT_genre.items():
    tmp_perc = value / total_games_ratingT * 100
    if tmp_perc > 5.5:
        percentage.append(tmp_perc)
        genre.append(key)
    else:
        misc_perc = misc_perc + tmp_perc
        
percentage.append(misc_perc)
genre.append('Rest')       

m = max(percentage)
index = [i for i, j in enumerate(percentage) if j == m]
explode = [0] * len(percentage)
explode[index[0]] = 0.2

plt.pie(percentage, labels=genre, autopct='%1.1f%%', startangle=90, explode = explode)
plt.title('Percentage of genre in T (Teenager+13) Rating Category')
plt.savefig(os.getcwd()+'\\rating_pie_T.png', dpi=1000)
plt.show()

# Rating M
percentage = []
genre = []
misc_perc = 0
total_games_ratingM = mydict_rating.get('M')

for key, value in mydict_ratingM_genre.items():
    tmp_perc = value / total_games_ratingM * 100
    if tmp_perc > 3:
        percentage.append(tmp_perc)
        genre.append(key)
    else:
        misc_perc = misc_perc + tmp_perc

percentage.append(misc_perc)
genre.append('Rest')

m = max(percentage)
index = [i for i, j in enumerate(percentage) if j == m]
explode = [0] * len(percentage)
explode[index[0]] = 0.2

plt.pie(percentage, labels=genre, autopct='%1.1f%%', startangle=90, explode = explode)
plt.title('Percentage of genre in M (Mature+17) Rating Category')
plt.savefig(os.getcwd()+'\\rating_pie_M.png', dpi=1000)
plt.show()

# Plot sales shooting and COD
plt.figure()
plt.title('Shooter genre market analysis')
plt.plot(mylist_time, sales_genre_years[3], '-', label = mylist_genre[3][0])
plt.plot(mylist_time, sales_cod_years, '-', label = 'COD')

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()
plt.savefig(os.getcwd()+'\\shooter_monopoly.png', dpi=1000)
plt.show()

# Plot sales action and GTA
plt.figure()
plt.title('Action genre market analysis')
plt.plot(mylist_time, sales_genre_years[9], '-', label = mylist_genre[9][0])
plt.plot(mylist_time, sales_gta_years, '-', label = 'GTA')

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()
plt.savefig(os.getcwd()+'\\action_monopoly.png', dpi=1000)
plt.show()

# Plot sales sports and FIFA
plt.figure()
plt.title('Sports genre market analysis')
plt.plot(mylist_time, sales_genre_years[0], '-', label = mylist_genre[0][0])
plt.plot(mylist_time, sales_fifa_years, '-', label = 'FIFA')
plt.plot(mylist_time, sales_wiisf_years, '-', label = 'Wii Sports / Wii Fit')

plt.grid()
plt.xticks(rotation=30)
plt.legend(prop={'size': 6})
plt.gca().set_xlim([mylist_time[0], mylist_time[-1]]) 
plt.ylabel('Copies sold (in millions)')
plt.xlabel('Game launching year')
plt.tight_layout()
plt.savefig(os.getcwd()+'\\sports_monopoly.png', dpi=1000)
plt.show()

# Publisher NA
percentage = []
publisher_labels = []
sales_tot_NA = sum(sum(sales_genre_years_NA))
for i in range(n_top):
    publisher_labels.append(mylist_publisher[i][-1])
    tmp_perc = sales_publisher_NA[i] / sales_tot_NA * 100
    percentage.append(tmp_perc)

m = max(percentage)
index = [i for i, j in enumerate(percentage) if j == m]
explode = [0] * len(percentage)
explode[index[0]] = 0.2

rest_perc = 100 - sum(percentage)
percentage.append(rest_perc)
publisher_labels.append('Rest')

explode.append(0)

plt.pie(percentage, labels=publisher_labels, autopct='%1.1f%%', startangle=90, explode = explode)
plt.title('Distribution of sales per publisher North America (Top 5)')
plt.savefig(os.getcwd()+'\\publisher_pie_NA.png', dpi=1000)
plt.show()

# Publisher Europe
percentage = []
publisher_labels = []
sales_tot_PAL = sum(sum(sales_genre_years_PAL))
for i in range(n_top):
    publisher_labels.append(mylist_publisher[i][-1])
    tmp_perc = sales_publisher_PAL[i] / sales_tot_PAL * 100
    percentage.append(tmp_perc)

m = max(percentage)
index = [i for i, j in enumerate(percentage) if j == m]
explode = [0] * len(percentage)
explode[index[0]] = 0.2

rest_perc = 100 - sum(percentage)
percentage.append(rest_perc)
publisher_labels.append('Rest')

explode.append(0)

plt.pie(percentage, labels=publisher_labels, autopct='%1.1f%%', startangle=90, explode = explode)
plt.title('Distribution of sales per publisher Europe (Top 5)')
plt.savefig(os.getcwd()+'\\publisher_pie_PAL.png', dpi=1000)
plt.show()

# Publisher Japan
percentage = []
publisher_labels = []
sales_tot_JP = sum(sum(sales_genre_years_JP))
for i in range(n_top):
    if mylist_publisher[i][-1] == 'Nintendo' or mylist_publisher[i][-1] == 'Konami':
        publisher_labels.append(mylist_publisher[i][-1])
        tmp_perc = sales_publisher_JP[i] / sales_tot_JP * 100
        percentage.append(tmp_perc)
    elif mylist_publisher[i][-1] == 'Electronic Arts':
        publisher_labels.append('EA')
        tmp_perc = sales_publisher_JP[i] / sales_tot_JP * 100
        percentage.append(tmp_perc)        
    
m = max(percentage)
index = [i for i, j in enumerate(percentage) if j == m]
explode = [0] * len(percentage)
explode[index[0]] = 0.2

rest_perc = 100 - sum(percentage)
percentage.append(rest_perc)
publisher_labels.append('Rest')

explode.append(0)

plt.pie(percentage, labels=publisher_labels, autopct='%1.1f%%', startangle=90, explode = explode, textprops={'fontsize': 8})
plt.title('Distribution of sales per publisher Japan (Top 3)')
plt.savefig(os.getcwd()+'\\publisher_pie_JP.png', dpi=1000)
plt.show()

# Activison (Platform)
percentage = []
platform = []
misc_perc = 0
total_games_Act = mylist_publisher[index_activision][0]

for key, value in platform_activision.items():
    tmp_perc = value / float(total_games_Act) * 100
    if tmp_perc > 4:
        percentage.append(tmp_perc)
        platform.append(key)
    else:
        misc_perc = misc_perc + tmp_perc

percentage.append(misc_perc)
platform.append('Rest')

plt.pie(percentage, labels=platform, autopct='%1.1f%%', startangle=90)
plt.title('Games distributed by Activision per platform')
plt.savefig(os.getcwd()+'\\activision_platform.png', dpi=1000)
plt.show()

# Activison (Genre)
percentage = []
genre = []
misc_perc = 0
total_games_Act = mylist_publisher[index_activision][0]

for key, value in genre_activision.items():
    tmp_perc = value / float(total_games_Act) * 100
    if tmp_perc > 4:
        percentage.append(tmp_perc)
        genre.append(key)
    else:
        misc_perc = misc_perc + tmp_perc

percentage.append(misc_perc)
genre.append('Rest')

plt.pie(percentage, labels=genre, autopct='%1.1f%%', startangle=90)
plt.title('Games distributed by Activision per genre')
plt.savefig(os.getcwd()+'\\activision_genre.png', dpi=1000)
plt.show()

# Konami (Platform)
percentage = []
platform = []
misc_perc = 0
total_games_konami = mylist_publisher[index_konami][0]

for key, value in platform_konami.items():
    tmp_perc = value / float(total_games_konami) * 100
    if tmp_perc > 4:
        percentage.append(tmp_perc)
        platform.append(key)
    else:
        misc_perc = misc_perc + tmp_perc

percentage.append(misc_perc)
platform.append('Rest')

plt.pie(percentage, labels=platform, autopct='%1.1f%%', startangle=90)
plt.title('Games distributed by Konami per platform')
plt.savefig(os.getcwd()+'\\konami_platform.png', dpi=1000)
plt.show()

# Nintendo (Platform)
percentage = []
platform = []
misc_perc = 0
total_games_nintendo = mylist_publisher[index_nintendo][0]

for key, value in platform_nintendo.items():
    tmp_perc = value / float(total_games_nintendo) * 100
    if tmp_perc > 6:
        percentage.append(tmp_perc)
        platform.append(key)
    else:
        misc_perc = misc_perc + tmp_perc

percentage.append(misc_perc)
platform.append('Rest')

plt.pie(percentage, labels=platform, autopct='%1.1f%%', startangle=90)
plt.title('Games distributed by Nintendo per platform')
plt.savefig(os.getcwd()+'\\nintendo_platform.png', dpi=1000)
plt.show()


# Sales per geography
plt.title('Total sales per geographic region (1990-2019)')
height = [sum(sales_years_NA), sum(sales_years_PAL), sum(sales_years_JP)]
bars = ('North America', 'Europe', 'Japan')
 
y_pos = [0,2,4]
plt.ylabel('Copies sold (in millions)')
plt.bar(y_pos, height, color=['blue', 'orange', 'green'],  edgecolor='black')
plt.xticks(y_pos, bars)

plt.savefig(os.getcwd()+'\\geography_study.png', dpi=1000)
plt.show()

# Sales per geography per population
plt.title('Sales per population per geographic region (1990-2019)')
height = [sum(sales_years_NA)/population_NA, sum(sales_years_PAL)/population_PAL, sum(sales_years_JP)/population_JP]
bars = ('North America', 'Europe', 'Japan')
 
y_pos = [0,2,4]
plt.bar(y_pos, height, color=['blue', 'orange', 'green'],  edgecolor='black')
plt.xticks(y_pos, bars)
plt.ylabel('Copies sold per citizen')

plt.savefig(os.getcwd()+'\\geography_study_popul.png', dpi=1000)
plt.show()

# Sales per rating NA
plt.title('Sales per ESRB Rating NA (1990-2019)')
height = [sales_rating_tot_NA[0], sales_rating_tot_NA[3], sales_rating_tot_NA[4], sales_rating_tot_NA[2]]
bars = ('Everyone', 'Everyone +10', 'Teenager +13', 'Mature +17')
 
y_pos = [0,2,4,6]
plt.ylabel('Copies sold (in millions)')
plt.bar(y_pos, height, color=['blue', 'orange', 'green', 'red'],  edgecolor='black')
plt.xticks(y_pos, bars)

plt.savefig(os.getcwd()+'\\esrb_rating_study_NA.png', dpi=1000)
plt.show()

# Sales per rating Europe
plt.title('Sales per ESRB Rating Europe (1990-2019)')
height = [sales_rating_tot_PAL[0], sales_rating_tot_PAL[3], sales_rating_tot_PAL[4], sales_rating_tot_PAL[2]]
bars = ('Everyone', 'Everyone +10', 'Teenager +13', 'Mature +17')
 
y_pos = [0,2,4,6]
plt.ylabel('Copies sold (in millions)')
plt.bar(y_pos, height, color=['blue', 'orange', 'green', 'red'],  edgecolor='black')
plt.xticks(y_pos, bars)

plt.savefig(os.getcwd()+'\\esrb_rating_study_PAL.png', dpi=1000)
plt.show()

# Sales per rating Japan
plt.title('Sales per ESRB Rating Japan (1990-2019)')
height = [sales_rating_tot_JP[0], sales_rating_tot_JP[3], sales_rating_tot_JP[4], sales_rating_tot_JP[2]]
bars = ('Everyone', 'Everyone +10', 'Teenager +13', 'Mature +17')
 
y_pos = [0,2,4,6]
plt.ylabel('Copies sold (in millions)')
plt.bar(y_pos, height, color=['blue', 'orange', 'green', 'red'],  edgecolor='black')
plt.xticks(y_pos, bars)

plt.savefig(os.getcwd()+'\\esrb_rating_study_JP.png', dpi=1000)
plt.show()

# Sales per rating
plt.title('Total sales per ESRB Rating (1990-2019)')
height = [sales_rating_tot_world[2], sales_rating_tot_world[0]+sales_rating_tot_world[3]+sales_rating_tot_world[4]]
bars = ('Adults only', 'Rest')
 
y_pos = [0,2]
plt.ylabel('Copies sold (in millions)')
plt.bar(y_pos, height, color=['red', 'blue'],  edgecolor='black')
plt.xticks(y_pos, bars)

plt.savefig(os.getcwd()+'\\esrb_rating_study.png', dpi=1000)
plt.show()

