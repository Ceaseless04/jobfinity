import pandas as pd

df = pd.read_csv('ResumeDataSet2_transformed.csv')

print(df['Category'].unique())

