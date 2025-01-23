import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from matplotlib.pyplot import winter

import preprocessing,helper

user_menu = st.sidebar.radio(
    'Select Options',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete-wise Analysis')
)

summer_df, winter_df=preprocessing.preprocess()
season=['Summer','Winter']

if user_menu == 'Medal Tally':
    select_season = st.selectbox("Select Season ", season)
    if select_season == 'Summer':
        games, country, cities, event, sport = helper.get_values(summer_df)
    else:
        games, country, cities, event, sport = helper.get_values(winter_df)
    st.sidebar.header('Medal Tally')
    select_game = st.sidebar.selectbox("Select Game ", games)
    select_country = st.sidebar.selectbox("Select Country ", country)
    if select_game == 'Overall' and select_country == 'Overall':
        st.title('Overall Performance')
    if select_game != 'Overall' and select_country == 'Overall':
        st.title('Overall Performance at ' + str(select_game) + ' Olympics')
    if select_game == 'Overall' and select_country != 'Overall':
        st.title(select_country + ' Overall Performance')
    if select_game != 'Overall' and select_country != 'Overall':
        st.title(select_country + ' Performance at ' + str(select_game) + ' Olympics')
    if select_season=='Summer':
        medals = helper.games_country_medal(summer_df,select_game,select_country)
    else:
        medals = helper.games_country_medal(winter_df,select_game,select_country)
    st.table(medals)

if user_menu == 'Overall Analysis':
    st.sidebar.header('Overall Analysis')
    st.title('Edition')
    select_season = st.sidebar.selectbox("Select Season ", season)
    if select_season == 'Summer':
        games, country, cities, event, sport = helper.get_values(summer_df)
    else:
        games, country, cities, event, sport = helper.get_values(winter_df)
    st.title('Participating Nations in ' +select_season+ ' Olympics')
    if select_season == 'Summer':
        edition_fig = helper.plot_edition(summer_df)
    else:
        edition_fig = helper.plot_edition(winter_df)
    st.plotly_chart(edition_fig)
    st.title('All Events Across ' + select_season + ' Olympics')
    if select_season == 'Summer':
        temp_df = summer_df.drop_duplicates(['Year', 'Sport', 'Event'])
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(temp_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
        st.pyplot(fig)
    else:
        temp_df = winter_df.drop_duplicates(['Year', 'Sport', 'Event'])
        fig,ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(temp_df.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),annot=True)
        st.pyplot(fig)
    select_sport = st.selectbox("Select Sport ", sport)
    st.title('Top 10 Athletes ' +select_sport)
    if select_sport == 'Overall':
        if select_season == 'Summer':
            temp_df = summer_df.dropna(subset=['Medal'])
            players_df = summer_df[['Name', 'Sport', 'Team']]
            players_df.drop_duplicates(inplace=True)
            x = temp_df['Name'].value_counts().reset_index().merge(players_df, on='Name', how='left')
        else:
            temp_df = winter_df.dropna(subset=['Medal'])
            players_df = winter_df[['Name', 'Sport', 'Team']]
            players_df.drop_duplicates(inplace=True)
            x = temp_df['Name'].value_counts().reset_index().merge(players_df, on='Name', how='left')
    else:
        if select_season == 'Summer':
            temp_df = summer_df[summer_df['Sport'] == select_sport]
            temp_df = temp_df.dropna(subset=['Medal'])
            players_df = summer_df[['Name', 'Sport','Team']]
            players_df.drop_duplicates(inplace=True)
            x = temp_df['Name'].value_counts().reset_index().merge(players_df, on='Name', how='left')
        else:
            temp_df = winter_df[winter_df['Sport'] == select_sport]
            temp_df = temp_df.dropna(subset=['Medal'])
            players_df = winter_df[['Name', 'Sport','Team']]
            players_df.drop_duplicates(inplace=True)
            x = temp_df['Name'].value_counts().reset_index().merge(players_df, on='Name', how='left')
    st.table(x.head(10))

if user_menu == 'Country-wise Analysis':
    st.sidebar.header('Country-wise Analysis')
    st.title('Country-wise Analysis')
    select_season = st.sidebar.selectbox("Select Season ", season)
    if select_season == 'Summer':
        games, country, cities, event, sport = helper.get_values(summer_df)
    else:
        games, country, cities, event, sport = helper.get_values(winter_df)
    select_country = st.sidebar.selectbox("Select Country ", country[1:])
    st.title('Medal Tally for '+select_country)
    if select_season == 'Summer':
        temp_df = summer_df.dropna(subset=['Medal'])
        temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Event','Sport','Medal'], inplace=True)
        country_df = temp_df[temp_df['region'] == select_country]
        country_medal = country_df.groupby('Games').count()['Medal'].reset_index()
        country_fig = px.line(country_medal, x='Games', y='Medal')
    else:
        temp_df = winter_df.dropna(subset=['Medal'])
        temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Event', 'Sport', 'Medal'],inplace=True)
        country_df = temp_df[temp_df['region'] == select_country]
        country_medal = country_df.groupby('Games').count()['Medal'].reset_index()
        country_fig = px.line(country_medal, x='Games', y='Medal')
    st.plotly_chart(country_fig)

    st.title('Medal Heatmap for '+select_country)
    if select_season == 'Summer':
        temp_df = summer_df[summer_df['region'] == select_country].dropna(subset=['Medal'])
        temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Event', 'Sport', 'Medal'],inplace=True)
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int'),annot=True)
        st.pyplot(fig)
    else:
        temp_df = summer_df[summer_df['region'] == select_country].dropna(subset=['Medal'])
        temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Event', 'Sport', 'Medal'],inplace=True)
        fig, ax = plt.subplots(figsize=(20, 20))
        ax = sns.heatmap(temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int'), annot=True)
        st.pyplot(fig)

    st.title('Top 10 Athletes of ' +select_country)
    if select_season == 'Summer':
        temp_df = summer_df[summer_df['region'] == select_country]
        temp_df = temp_df.dropna(subset=['Medal'])
        players_df = summer_df[['Name', 'Sport']]
        players_df.drop_duplicates(inplace=True)
        x = temp_df['Name'].value_counts().reset_index().merge(players_df, on='Name', how='left')
    else:
        temp_df = winter_df[winter_df['region'] == select_country]
        temp_df = temp_df.dropna(subset=['Medal'])
        players_df = winter_df[['Name', 'Sport']]
        players_df.drop_duplicates(inplace=True)
        x = temp_df['Name'].value_counts().reset_index().merge(players_df, on='Name', how='left')
    st.table(x.head(10))

if user_menu == 'Athlete-wise Analysis':
    st.sidebar.header('Athlete-wise Analysis')
    st.title('Athlete-wise Analysis')
    select_season = st.sidebar.selectbox("Select Season ", season)
    st.title('Age-wise Medal Distribution Graph')
    if select_season == 'Summer':
        x1 = summer_df['Age'].dropna()
        x2 = summer_df[summer_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = summer_df[summer_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = summer_df[summer_df['Medal'] == 'Bronze']['Age'].dropna()
        summer_fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age Distribution', 'Gold Medalist Age Distribution',
                                                           'Silver Medalist Age Distribution', 'Bronze Medalist Age Distribution'], show_hist=False, show_rug=False)
        st.plotly_chart(summer_fig)
    else:
        x1 = winter_df['Age'].dropna()
        x2 = winter_df[winter_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = winter_df[winter_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = winter_df[winter_df['Medal'] == 'Bronze']['Age'].dropna()
        summer_fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age Distribution', 'Gold Medalist Age Distribution',
                                                           'Silver Medalist Age Distribution', 'Bronze Medalist Age Distribution'], show_hist=False, show_rug=False)
        st.plotly_chart(summer_fig)

    st.title('Sport-wise Gold Medal Distribution Graph')
    if select_season == 'Summer':
        sport = summer_df['Sport'].drop_duplicates().dropna().tolist()
        summer_sports = []
        summer_gold_medalist = []
        for i in sport:
            temp_df = summer_df[summer_df['Sport'] == i]
            sport_medals = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
            if sport_medals.count() > 2:
                summer_gold_medalist.append(sport_medals.tolist())
                summer_sports.append(i)
        summer_sport_fig = ff.create_distplot(summer_gold_medalist, summer_sports, show_hist=False, show_rug=False)
        st.plotly_chart(summer_sport_fig)
    else:
        sport = winter_df['Sport'].drop_duplicates().dropna().tolist()
        winter_sports = []
        winter_gold_medalist = []
        for i in sport:
            temp_df = summer_df[summer_df['Sport'] == i]
            sport_medals = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
            if sport_medals.count() > 1:
                winter_gold_medalist.append(sport_medals.tolist())
                winter_sports.append(i)
        winter_sport_fig = ff.create_distplot(winter_gold_medalist, winter_sports, show_hist=False, show_rug=False)
        st.plotly_chart(winter_sport_fig)

    st.title('Sex-wise Distribution Graph')
    if select_season == 'Summer':
        summer_men = summer_df[summer_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
        summer_women = summer_df[summer_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
        summer_final_count = summer_men.merge(summer_women, on='Year', how='left')
        summer_final_count.fillna(0, inplace=True)
        summer_final_count.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
        summer_final_fig = px.line(summer_final_count, x='Year', y=['Male', 'Female'])
        st.plotly_chart(summer_final_fig)
    else:
        winter_men = winter_df[winter_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
        winter_women = winter_df[winter_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
        winter_final_count = winter_men.merge(winter_women, on='Year', how='left')
        winter_final_count.fillna(0, inplace=True)
        winter_final_count.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
        winter_final_fig = px.line(winter_final_count, x='Year', y=['Male', 'Female'])
        st.plotly_chart(winter_final_fig)