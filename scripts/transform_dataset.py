import pandas as pd

# Read ResumeDataSet2.csv
df = pd.read_csv('ResumeDataSet2.csv')

# Add an ID column (sequential numbers)
df['ID'] = range(1, len(df) + 1)

# Rename the 'Resume' column to 'Resume_str'
df = df.rename(columns={'Resume': 'Resume_str'})

# Add an empty 'Resume_html' column
df['Resume_html'] = ''

# Reorder columns to match Resume.csv structure
df = df[['ID', 'Resume_str', 'Resume_html', 'Category']]

# Save the transformed data
df.to_csv('ResumeDataSet2_transformed.csv', index=False)

print("Transformation complete. Output saved to ResumeDataSet2_transformed.csv") 