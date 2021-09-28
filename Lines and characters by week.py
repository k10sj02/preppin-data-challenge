# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 13:57:48 2021

@author: kelly.gilbert
"""


from numpy import nan, where
from pandas import concat, DataFrame
import requests


def create_chart(df, colname, highlight_col=None, highlight_val=None):
    """
    output a horizontal bar chart of colname. If highlight_col is provided, matching bars 
    are highlighted
    """
    
    df = df.sort_values(colname, ascending=True)
    df[colname]=df[colname].round(0)
    
    if highlight_col != None:
        df['highlight_colors'] = where(df[highlight_col]==highlight_val, 'darkorange', 'silver')
   
    # bar plot
    ax = df.plot.barh(x='week', y=colname, figsize=(6,10), color=list(df['highlight_colors']),
                 title=f'Preppin\' Data {colname.replace("_", " ").title()} by Week\n', 
                 legend=False, label=colname, width=0.7)
    
    # add the labels
    spacer = df[colname].max() * 0.02
    for p in ax.patches:
        b = p.get_bbox()
        ax.annotate(int(b.x1-b.x0), ((b.x1 - b.x0) + spacer, b.y0))


# --------------------------------------------------------------------------------------------------
# import all of the .py file contents from github (one row = one week)
# --------------------------------------------------------------------------------------------------

year = 2021
max_week = 38

df = None
for w in range(1,max_week + 1):
    r = requests.get(f'https://raw.githubusercontent.com/kelly-gilbert/preppin-data-challenge/master/{year}/preppin-data-{year}-{("00" + str(w))[-2:]}/preppin-data-{year}-{("00" + str(w))[-2:]}.py')
    df = concat([df, DataFrame({ 'week' : [w], 'text' : [r.text] })])
df.reset_index(drop=True, inplace=True)


# --------------------------------------------------------------------------------------------------
# parse the script text
# --------------------------------------------------------------------------------------------------

# replace trailing spaces and newlines with pipe
df['main_script'] = df['text'].str.replace(r'\n', r'|')

# remove the results check section
df['main_script'] = df['main_script'].str.replace(r'(\|\s*)*#\s*-*\|# check results.*', '')

# remove everything above the imports
df['main_script'] = df['main_script'].str.replace(r'.*?\|(?=(?:import|from.*?import))', '')


# split to lines to rows
df['lines'] = df['main_script'].str.split('|')
df_e = df.explode('lines')
df_e['lines'] = df_e['lines'].str.strip()


# identify the line types and lengths
df_e['comment'] = where(df_e['lines'].str[0] == '#', df_e['lines'].str.len(), nan)
df_e['blank'] = where(df_e['lines'] == '', df_e['lines'].str.len(), nan)
df_e['code'] = where(df_e['comment'].isna() & df_e['blank'].isna(), df_e['lines'].str.len(), nan)
df_e['line_length'] = df_e['lines'].str.len()


# --------------------------------------------------------------------------------------------------
# summarize by week
# --------------------------------------------------------------------------------------------------

# counts by file
df_agg = df_e.groupby('week').agg(total_lines=('week', 'count'),
                                  code_lines=('code', 'count'),
                                  comment_lines=('comment', 'count'),
                                  blank_lines=('blank', 'count'),
                                  total_chars=('line_length', 'sum'),
                                  code_chars=('code', 'sum')).reset_index()


# --------------------------------------------------------------------------------------------------
# plots
# --------------------------------------------------------------------------------------------------

create_chart(df_agg, 'total_chars', highlight_col='week', highlight_val=37)
create_chart(df_agg, 'code_chars', highlight_col='week', highlight_val=37)
create_chart(df_agg, 'total_lines', highlight_col='week', highlight_val=37)
create_chart(df_agg, 'code_lines', highlight_col='week', highlight_val=37)
