import pandas as pd

df4 = pd.read_csv('books.csv')
df = df4[['Genre', 'Name', 'Author', 'Price', 'Year']]


df1 = df.iloc[:200]
df1.index.names = ['id']

df2 = df[200:]
df2.drop_duplicates()
df2 = df2[~df2['Name'].isin(df1['Name'])]
df2.index.names = ['id']



df1.to_csv('Book_Info.txt', header=None, index='id', sep='|')
df2.to_csv('Book_Recommendations.txt', header=None, index='id', sep='|')