# Deliverable 1

## Source
TMDB data and I get data by using their API calls

## Shape
4776*27

## Numeric: Non-Numeric
7: 27


## What is your plan for the non-numeric features? 
I will encode categorical variables (like genres or status) using One-Hot Encoding

## One potential target feature of your dataset: 
revenue

## One-line problem statement with respect to the target feature: 
Develop a predictive model to estimate a film's global box office revenue based on its metadata, budget, and pre-release popularity metrics.

# Data Quality Assessment

## Is the dataset already cleaned? 
No.

## What are some inconsistencies your dataset has? 
The dataset contains "nested" data structures (JSON-like strings in genres and production_companies) that require flattening, mixed currency formats, and inconsistent date formatting.

## Does the dataset have missing values that need cleaning? 
Yes.

There are significant gaps in homepage, tagline, and belongs_to_collection, as well as null entries in the runtime and release_date columns for unreleased or obscure titles.