# keep only the categories that are in the list
# DS, Web Design, Java Developer, SAP Developer, Python Developer, DevOps Engineer, Database, ETL Developer, DotNet Developer, Blockchain, and testing

import pandas as pd

df = pd.read_csv('ResumeDataSet2_transformed.csv')

df = df[df['Category'].isin(['DS', 'Web Design', 'Java Developer', 'SAP Developer', 'Python Developer', 'DevOps Engineer', 'Database', 'ETL Developer', 'DotNet Developer', 'Blockchain', 'testing'])]

df.to_csv('ResumeDataSet2_transformed_filtered.csv', index=False)
