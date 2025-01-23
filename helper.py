import plotly.express as px
from matplotlib import pyplot as plt
import seaborn as sns
import streamlit as st

def get_values(df):
    games = df['Games'].unique().tolist()
    games.sort()
    games.insert(0,'Overall')
    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'Overall')
    cities = df['City'].unique().tolist()
    cities.sort()
    # cities.insert(0, 'All')
    event = df['Event'].unique().tolist()
    event.insert(0, 'All')
    sport = df['Sport'].unique().tolist()
    sport.insert(0, 'Overall')
    return games, country, cities, event, sport

def games_country_medal(df,games,country):
    flag=0
    temp_df=None
    df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    if games == 'Overall' and country == 'Overall':
        temp_df = df
    elif games != 'Overall' and country == 'Overall':
        temp_df = df[df['Games'] == games]
    elif games == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = df[df['region'] == country]
    elif games != 'Overall' and country != 'Overall':
        temp_df = df[(df['Games'] == games) & (df['region'] == country)]

    if flag == 1:
        temp_df = temp_df.groupby('Games').sum()[['Gold','Silver','Bronze']].sort_values('Games')
    else:
        temp_df = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False)
    temp_df['Total'] = temp_df['Gold'] + temp_df['Silver'] + temp_df['Bronze']
    return temp_df

def plot_edition(df):
    nation_count = df.drop_duplicates(['Games', 'region'])['Games'].value_counts().reset_index().sort_values('Games')
    nation_count.rename(columns={'count': 'Number of Countries'}, inplace=True)
    edition_fig = px.line(nation_count, x='Games', y='Number of Countries')
    return edition_fig

def plot_events(df):
    temp_df = df.drop_duplicates(['Year', 'Sport', 'Event'])
    return temp_df