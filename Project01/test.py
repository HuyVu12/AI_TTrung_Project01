import pandas as pd
import numpy as np

df = pd.read_csv('./data/Salary Data.csv')

x = df.drop(columns=['Salary'])
x['Gender'] = x['Gender'].astype('category')
x['Gender'] = x['Gender'].cat.codes

x['Education Level'] = x['Education Level'].astype('category')
x['Education Level'] = x['Education Level'].cat.codes

x['Job Title'] = x['Job Title'].astype('category')
x['Job Title'] = x['Job Title'].cat.codes

y = df['Salary']

print(df.columns)

# df['Education Level'] = df['Education Level'].astype('category')

# key = "Master's"
# print(df['Education Level'].cat.categories.get_loc(key))

print(np.array(df['Job Title']))
