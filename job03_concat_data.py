import pandas as pd

# 1. 정치 (Politics)
df = pd.read_csv('data/naver_news_politics.csv')
print(df.head())

# [추가] 지난주 정치/경제 통합 파일 병합
df_temp = pd.read_csv('data/naver_news_politics_economics_20260604.csv')
df = pd.concat([df, df_temp], ignore_index=True)

# 2. 경제 (Economic)
df_temp = pd.read_csv('data/naver_news_economics.csv')
print(df_temp.head())
df = pd.concat([df, df_temp], ignore_index=True)

# 3. 사회 (Social)
df_temp = pd.read_csv('data/naver_news_social.csv')
df = pd.concat([df, df_temp], ignore_index=True)

# [추가] 지난주 사회 파일 병합
df_temp = pd.read_csv('data/naver_news_social_20260604.csv')
df = pd.concat([df, df_temp], ignore_index=True)

# 4. 문화 (Culture)
df_temp = pd.read_csv('data/naver_news_culture.csv')
df = pd.concat([df, df_temp], ignore_index=True)

# [추가] 지난주 문화 파일 병합
df_temp = pd.read_csv('data/naver_news_culture_20260604.csv')
df = pd.concat([df, df_temp], ignore_index=True)

# 5. 세계 (World)
df_temp = pd.read_csv('data/naver_news_world.csv')
df = pd.concat([df, df_temp], ignore_index=True)

# [추가] 지난주 세계 파일 병합
df_temp = pd.read_csv('data/naver_news_world_20260604.csv')
df = pd.concat([df, df_temp], ignore_index=True)

# 6. IT (IT)
df_temp = pd.read_csv('data/naver_news_IT.csv')
df = pd.concat([df, df_temp], ignore_index=True)

# [수정] 올바른 지난주 IT 파일명으로 변경 완료
df_temp = pd.read_csv('data/naver_news_IT_20260604.csv')
df = pd.concat([df, df_temp], ignore_index=True)

df.info()
df = df.drop_duplicates()
df.reset_index(drop=True, inplace=True)

print(df.category.value_counts())
print(df.isnull().sum())
df.info()

# 결과 파일 이름 유지
df.to_csv('./data/news_titles.csv', index=False)