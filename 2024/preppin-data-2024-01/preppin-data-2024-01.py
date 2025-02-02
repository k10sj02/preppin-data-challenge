# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 01 - Prep Air's Flow Card
https://preppindata.blogspot.com/2024/01/2024-week-1-prep-airs-flow-card.html

- Input the data
- Split the Flight Details field to form:
  - Date 
  - Flight Number
  - From
  - To
  - Class
  - Price
- Convert the following data fields to the correct data types:
  - Date to a date format
  - Price to a decimal value
- Change the Flow Card field to Yes / No values instead of 1 / 0
- Create two tables, one for Flow Card holders and one for non-Flow Card holders
- Output the data sets

Author: Kelly Gilbert
Created: 2024-01-08
Requirements:
  - input dataset:
      - PD 2024 Wk 1 Input.csv
  - output dataset (for results check only):
      - PD 2024 Wk 1 Output Flow Card.csv
      - PD 2024 Wk 1 Output Non-Flow Card.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# constants
#---------------------------------------------------------------------------------------------------

FLIGHT_DETAILS_COLS = ['Date', 'Flight Number', 'From', 'To', 'Class', 'Price']

REPLACE_VALS = { 1 : 'Yes', 
                 0 : 'No' }

FILE_SUFFIX = { 'Yes' : 'Flow Card',
                'No' : 'Non-Flow Card' }


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\PD 2024 Wk 1 Input.csv')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# parse the flight details column
df[FLIGHT_DETAILS_COLS] = df['Flight Details'].str.extract(r'(.*)//(.*)//(.*)-(.*)//(.*)//(.*)')


# change data types
df['Date'] = pd.to_datetime(df['Date'])
df['Price'] = df['Price'].astype(float)


# replace Flow Card values
REPLACE_VALS = { 1 : 'Yes', 0 : 'No' }
df['Flow Card?'] = df['Flow Card?'].replace(REPLACE_VALS)


#---------------------------------------------------------------------------------------------------
# output the files
#---------------------------------------------------------------------------------------------------

FILE_SUFFIX = { 'Yes' : 'Flow Card',
                'No' : 'Non-Flow Card' }

for f in df['Flow Card?'].unique():
    ( df[df['Flow Card?']==f]
        .drop(columns='Flight Details')
        .to_csv(fr'.\outputs\output-2024-01-{FILE_SUFFIX[f] if f in FILE_SUFFIX.keys() else f}.csv', 
                index=False,
                date_format='%d/%m/%Y')
    )


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

cols = ['Flow Card?', 'Bags Checked', 'Meal Type', 'Date', 'Flight Number', 
        'From', 'To', 'Class', 'Price']
solution_files = [r'.\outputs\PD 2024 Wk 1 Output Flow Card.csv', 
                  r'.\outputs\PD 2024 Wk 1 Output Non-Flow Card.csv']
my_files = [r'.\outputs\output-2024-01-Flow Card.csv',
            r'.\outputs\output-2024-01-Non-Flow Card.csv']
unique_cols = [cols, cols]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
