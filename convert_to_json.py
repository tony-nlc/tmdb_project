# Convert CSV files to JSON for Tableau
# Run this in your local Python: python convert_to_json.py

import pandas as pd
import json
import os

files = [
    'tableau_genre_summary.csv',
    'tableau_year_trends.csv', 
    'tableau_budget_revenue.csv',
    'tableau_month_genre.csv',
    'tableau_franchises.csv',
    'tableau_full_data.csv'
]

for f in files:
    if os.path.exists(f):
        df = pd.read_csv(f)
        json_name = f.replace('.csv', '.json')
        df.to_json(json_name, orient='records', indent=2)
        print(f"✅ Created {json_name}")
    else:
        print(f"⚠️  {f} not found")

print("\nAll JSON files created!")
