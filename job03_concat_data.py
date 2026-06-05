import pandas as pd
df = pd.read_csv('data/naver_news_social.csv')
print(df.head())
exit()
df_temp = pd.read_csv('data/naver_news_culture.csv')
df = pd.concat([df, df_temp])