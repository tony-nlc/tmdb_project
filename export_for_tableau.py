# ============================================
# Tableau Data Export Script
# Run this in your Jupyter notebook to generate Tableau-ready CSV files
# ============================================

import pandas as pd
import ast

# Load data
df = pd.read_csv('cleaned_tmdb_data.csv')

def extract_genres(genres_str):
    """Extract genre names from the genres column"""
    if pd.isna(genres_str):
        return []
    try:
        genres_list = ast.literal_eval(genres_str)
        return [g['name'] for g in genres_list]
    except:
        return []

# ============================================
# 1. Genre Summary (for bar charts, pie charts)
# ============================================
df['genre_list'] = df['genres'].apply(extract_genres)
df_exploded = df.explode('genre_list')
df_exploded = df_exploded[df_exploded['genre_list'].notna()]

genre_summary = df_exploded.groupby('genre_list').agg({
    'id': 'count',
    'budget': 'mean',
    'revenue': 'mean',
    'vote_average': 'mean',
    'popularity': 'mean'
}).rename(columns={
    'id': 'movie_count',
    'budget': 'avg_budget',
    'revenue': 'avg_revenue',
    'vote_average': 'avg_rating',
    'popularity': 'avg_popularity'
}).reset_index()

genre_summary.to_csv('tableau_genre_summary.csv', index=False)
print("✅ tableau_genre_summary.csv")

# ============================================
# 2. Year Trends (for line charts)
# ============================================
year_trends = df[df['release_year'].notna()].groupby('release_year').agg({
    'id': 'count',
    'budget': ['sum', 'mean'],
    'revenue': ['sum', 'mean'],
    'vote_average': 'mean',
    'popularity': 'mean'
}).reset_index()

year_trends.columns = ['year', 'movie_count', 'total_budget', 'avg_budget', 
                       'total_revenue', 'avg_revenue', 'avg_rating', 'avg_popularity']
year_trends = year_trends.sort_values('year')
year_trends.to_csv('tableau_year_trends.csv', index=False)
print("✅ tableau_year_trends.csv")

# ============================================
# 3. Budget vs Revenue (scatter plot)
# ============================================
scatter_df = df[(df['budget'] > 0) & (df['revenue'] > 0)][
    ['title', 'release_year', 'budget', 'revenue', 'vote_average', 'popularity', 'genres']
].copy()
scatter_df['primary_genre'] = scatter_df['genres'].apply(lambda x: extract_genres(x)[0] if extract_genres(x) else 'Unknown')
scatter_df.to_csv('tableau_budget_revenue.csv', index=False)
print("✅ tableau_budget_revenue.csv")

# ============================================
# 4. Month-Genre Heatmap Data
# ============================================
month_genre = df_exploded[df_exploded['release_month'].notna()].groupby(
    ['release_month', 'genre_list']
).agg({
    'revenue': 'mean',
    'id': 'count'
}).reset_index()
month_genre.columns = ['release_month', 'genre', 'avg_revenue', 'movie_count']
month_genre.to_csv('tableau_month_genre.csv', index=False)
print("✅ tableau_month_genre.csv")

# ============================================
# 5. Franchises
# ============================================
def extract_collection(collection_str):
    if pd.isna(collection_str):
        return 'No Collection'
    try:
        coll = ast.literal_eval(collection_str)
        return coll.get('name', 'No Collection')
    except:
        return 'No Collection'

df['collection'] = df['belongs_to_collection'].apply(extract_collection)
franchise_df = df[df['collection'] != 'No Collection'].copy()

franchise_summary = franchise_df.groupby('collection').agg({
    'id': 'count',
    'budget': 'mean',
    'revenue': 'mean',
    'vote_average': 'mean'
}).rename(columns={
    'id': 'movie_count',
    'budget': 'avg_budget',
    'revenue': 'avg_revenue',
    'vote_average': 'avg_rating'
}).reset_index()

franchise_summary = franchise_summary.sort_values('avg_revenue', ascending=False).head(20)
franchise_summary.to_csv('tableau_franchises.csv', index=False)
print("✅ tableau_franchises.csv")

# ============================================
# 6. Full Cleaned Dataset
# ============================================
tableau_full = df[[
    'title', 'release_year', 'release_month', 'budget', 'revenue',
    'vote_average', 'vote_count', 'popularity', 'runtime',
    'original_language', 'has_homepage', 'genres'
]].copy()
tableau_full['primary_genre'] = tableau_full['genres'].apply(
    lambda x: extract_genres(x)[0] if extract_genres(x) else 'Unknown'
)
tableau_full.to_csv('tableau_full_data.csv', index=False)
print("✅ tableau_full_data.csv")

print("\n🎉 All Tableau files generated!")
