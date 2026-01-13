import pandas as pd 
from df1_pandera_schema import D1Schema


df = pd.read_csv('data/data_1.csv')
print(df.dtypes)
df_panderized = D1Schema.validate(df)
print(df_panderized.dtypes)