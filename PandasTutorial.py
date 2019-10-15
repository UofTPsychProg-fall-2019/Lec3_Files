#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lecture 3 tutorial for PSY 1210 - Fall 2019

@author: katherine duncan
"""
#%%
"""
INTRODUCTION TO SERIES
"""
#%%
# Import all libraries needed for the tutorial
import os
import numpy as np # gives us arrays, matrices and some vectorized math
import pandas as pd # gives us dataframes that are easy to manipulate! Like R. It relies on NumPy

#%% 
# remember a numpy array?
my_array = np.array([1, 5, 3, 4, 3])

#%% 
# you can do some math with it

print('the mean is: ',str(my_array.mean()))
print('the max is: ',str(my_array.max()))
print('the sum is: ',str(my_array.sum()))

#%% 
# you arrange the values
my_array.sort()
my_array

# but which 3 is which 3????

#%% 
# pandas series are a lot like numpy arrays, but they have indices
# you can make one by inputting a list, np.array, or dictionary as the fist argument
my_series = pd.Series([1, 5, 3, 4, 3], name = 'score') 

#%% 
# this lets you keep track of your data
my_series.sort_values()
my_series


#%%
###############################################################################
# TRY IT YOURSELF:  TURN THIS list INTO A SERIES (be sure to give it a name)
###############################################################################

your_list = ['a', 'b', 'k', 'l', 's']
your_series = ...

#%% 
# you can also stack them to make a dataframe
# input a list of series or dataframes as the first arguement; 
# axis specifies how to stack them: 1 = stack horizontally and 0 = stack vertically   
our_df = pd.concat([my_series,your_series],axis=1) 
our_df

#%% 
"""
INTRODUCTION TO DATAFRAMES
"""

#%% 
# you can make a dataframe in lots of ways -- you don't have to make a series first
# you can use a dictionary 
df = pd.DataFrame({'Subject' : 1,
                    'Cond1' : [1]*5 + [2]*5,
                    'Cond2' : [1,2]*5,
                    'tNum' : range(1, 11),
                    'RT' : np.random.normal(500,100,10) })


#%%
# you can quickly learn things about your dataframe
df.dtypes
df.head()
df.describe()

#%%
# you can reoder your columns however you like
df2 = df[['Subject', 'Cond1', 'Cond2', 'RT', 'tNum']]
list(df2.columns)

#%%
# you can rename particular columns anything you like
df2 = df2.rename(columns={'tNum': 'Trial'})
list(df2.columns)

#%%
# you can sort it
df2 = df2.sort_values(by='Cond2')
df2.head()

#%%
# sort it by multiple variables 
df2 = df2.sort_values(by=['Cond2','RT'])
df2

#%%
# and put it back in the original order, thanks to the index!
df2 = df2.sort_index()
df2

#%%
# you can stack dataframes together
df3 = pd.DataFrame({'Subject' : 2,
                    'Cond1' : [1]*5 + [2]*5,
                    'Cond2' : [1,2]*5,
                    'Trial' : range(1, 11),
                    'RT' : np.random.normal(450,100,10) })

df = pd.concat([df2,df3],axis=0) # put your dataframes together in a list
df.head() # note that their columns don't need to be in the same order!


#%%
###############################################################################
# TRY IT YOURSELF! 
# MAKE A 3RD SUBJECT WITH A MEAN RT OF 550. ADD THE NEW SUBJECT TO THE OTHER 
# TWO SUBJECTS AND THEN REORDER THE COLUMNS HOWEVER YOU LIKE. SORT BY RT TO 
# FIND THE TRIAL WITH THE FASTEST RT
###############################################################################

df4 = pd.DataFrame(...)

#%% 
"""
USING PANDAS TO READ IN AND WRITE OUT FILES
"""

#%%
# let's now read in some data, like real scientists

# let's start by setting the data file location
# be sure to update your path to make this work
data_file = '/Users/katherineduncan/Documents/GitHub/PsychProgDev/lecture-files/lecture-files2019/Lec3/IAT_2018.csv'
# note that Windows users may need an "r" (e.g. r'\path') before their path string because "\" is a special character

# now let's read in the file
IAT = pd.read_csv(data_file)

# and take a look at the data
IAT.dtypes
IAT.shape
IAT.head()
IAT.describe()

# lets rename the key bias index 
IAT = IAT.rename(columns={'D_biep.White_Good_all':'D_white_bias'})

#%%
# pandas also makes it easy to write your dataframes as csvfiles
IAT.to_csv('filename.csv')

"""
INDEXING DATAFRAMES
"""
#%%
# there are several ways to select data from a dataframe
# .loc let's you use labels to select data in [index,column_name]

IAT.loc[0,'D_white_bias']

#%%
# you can also take slices of the dataframe using this notation
# note that these ranges are inclusive!
IAT.loc[0:3,'D_white_bias':'edu']

#%%
# alternatively you can use iloc to select data according to its position
IAT.iloc[0:4,3:6]

#%%
# something that can be tricky about pandas is there are a lot of ways to do the same thing
# for example all of these return the same output:
    
IAT.edu[0:5]
IAT['edu'][0:5]
IAT.loc[0:4,'edu']


#%%
###############################################################################
# TRY IT YOURSELF! 
# OUTPUT THE 10 LARGEST WHITE-GOOD BIASES BY SORTING THEN INDEXING
# TRY TO USE .ILOC AND .LOC TO SEE HOW THEY WORK DIFFERENTLY
###############################################################################                          

#%%
# logical or boolean idexing lets you select data based on specified requirements
# for example, you could select only white participants
IAT_white= IAT[IAT.raceomb_002==6]
IAT_white.describe()


#%%
# or white participants who identify as men
IAT_white_men = IAT[(IAT.raceomb_002==6) & (IAT.genderidentity=='[1]')]
IAT_white_men.describe()


#%%
# you can also easily create new columns
IAT['is_white'] = 1*(IAT.raceomb_002==6) #multiplying by 1 is a quick way to turn booleans into integers
IAT['is_black'] = 1*(IAT.raceomb_002==5)
IAT.describe()


#%%
###############################################################################
# TRY IT YOURSELF! 
# CREATE A NEW VARIABLE is_conservative THAT TAKES THE VALUE 1 WHEN PEOPLE 
# IDENTIFY AS STRONGLY OR MODERATELY CONSERVATIVE (VALUES 1 & 2 IN politicalid_7 VARIABLE)
###############################################################################     



#%%
"""
MISSING DATA
"""
#%%
# the dataset has a lot of missing values, which you can see using the .isnull() method
IAT.isnull().mean() #note that you can chain methods

# pandas is pretty savy though
# it skips over missing values when performing statistics
IAT.D_white_bias.mean()


#%%
# you can also drop rows that contain any missing values
IAT_noNaN = IAT.dropna(axis=0,how='any')
IAT_noNaN.isnull().mean()

#%%
"""
SIMPLE STATS
"""
#%%
# pandas makes basic descriptive stats easy
# it has methods for mean, median, mode, sum, std, count, min, max, prod, abs, and more! 
# you can calculate them for every column
IAT.mean(axis=0)

#%%
# or every row
IAT.sum(axis=1)

#%%
# and combine with logical indexing to get useful summaries
print ('conservative bias: ',IAT.loc[IAT.is_conservative==1,'D_white_bias'].mean())
print ('nonconservative bias: ',IAT.loc[IAT.is_conservative==0,'D_white_bias'].mean())

#%%
"""
PIVOT TABLES
"""
#%%
# but what you wanted some more complicated summaries, like looking at the white bias
# different race and political affiliations?
# you could write a loop to calculate these values, but pandas also has an easy way to do this!
# the pivot table function works a lot like pivot tables in excel, only you can automate them.

# you usually want to set values equal to your dependent variables
# index and columns equal to your independent and grouping variables
# you can use any numpy stat to summarize values
bias_table = pd.pivot_table(IAT, values = 'D_white_bias', 
                            index = ['politicalid_7'], 
                            columns = ['raceomb_002'], 
                            aggfunc=np.mean)
bias_table
# race coding:
 
"""
1	American Indian/Alaska Native
2	East Asian
3	South Asian
4	Native Hawaiian or other Pacific Islander
5	Black or African American
6	White
7	More than one race - Black/White
8	More than one race - Other
9	Other or Unknown
"""
#%%
# you can give multiple values to most of the arguements
bias_table = pd.pivot_table(IAT, values = ['D_white_bias'], 
                            index = ['politicalid_7'], 
                            columns = ['is_black','genderidentity'], 
                            aggfunc=np.mean)
print(bias_table)

#%%
# or select particular rows
bias_table_men = pd.pivot_table(IAT[IAT.genderidentity=='[1]'], values = ['D_white_bias'], 
                            index = ['politicalid_7'], 
                            columns = ['is_black'], 
                            aggfunc=np.mean)
print(bias_table_men)

#%%
# you can also add margins to your pivot table, which will tell you the row and column averages
bias_table = pd.pivot_table(IAT, values = ['D_white_bias'], 
                            index = ['politicalid_7'], 
                            columns = ['is_black','genderidentity'], 
                            aggfunc=np.mean,
                            margins=True)
print(bias_table)

#%%
###############################################################################
# TRY IT YOURSELF! 
# USING PIVOT TABLES CREATE CALCULATE HOW MEAN WHITE BIAS DEPENDS ON THE COMBINATION
# OF POLITICAL AFFILIATION AND EXPLICIT RACE ATTITUDES (att_7), BUT ONLY IN
# WHITE PARTICIPANTS 
###############################################################################    
bias_table = pd.pivot_table(...)
print(bias_table)


#%%
"""
CROSSTAB
"""
#%%
# another handy way to restructure your dataframe is using crosstab
# it computes a frequency table telling you how often values in different columns co-occur

counts = (pd.crosstab(IAT_white.politicalid_7, IAT_white.att_7))


#%%
# you can also normalize your frequency table across all cells or columns or rows
 
print(pd.crosstab(IAT_white.politicalid_7, IAT_white.att_7, normalize=True)) 
print(pd.crosstab(IAT_white.politicalid_7, IAT_white.att_7,  normalize='columns')) 
print(pd.crosstab(IAT_white.politicalid_7, IAT_white.att_7,  normalize='index')) 

#%%
"""
MERGING
"""
#%%
# first let's read in some more data containing info on when the data was collected
data_file = '/Users/katherineduncan/Documents/GitHub/PsychProgDev/lecture-files/lecture-files2019/Lec3/IAT_2018_time.csv'
IAT_time = pd.read_csv(data_file)

# merge allows us to combine this new information with our original data
IAT = pd.merge(IAT,IAT_time, on = 'session_id')
IAT.describe()

# note that merge has a lot of options to get things right when working with more complicated dataframes 

