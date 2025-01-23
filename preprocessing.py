import pandas as pd


def preprocess():
    summer_df = pd.read_csv('Athletes_summer_games.csv')
    winter_df = pd.read_csv('Athletes_winter_games.csv')
    region_df = pd.read_csv('noc_regions.csv')
    summer_df.drop_duplicates(inplace=True)
    winter_df.drop_duplicates(inplace=True)
    summer_df=summer_df.merge(region_df,on='NOC',how='left')
    winter_df = winter_df.merge(region_df, on='NOC', how='left')
    summer_df=pd.concat([summer_df,pd.get_dummies(summer_df['Medal'])],axis=1)
    summer_df['Bronze'] = summer_df['Bronze'].astype(int)
    summer_df['Silver'] = summer_df['Silver'].astype(int)
    summer_df['Gold'] = summer_df['Gold'].astype(int)
    winter_df = pd.concat([winter_df, pd.get_dummies(winter_df['Medal'])], axis=1)
    winter_df['Bronze'] = winter_df['Bronze'].astype(int)
    winter_df['Silver'] = winter_df['Silver'].astype(int)
    winter_df['Gold'] = winter_df['Gold'].astype(int)
    return summer_df, winter_df