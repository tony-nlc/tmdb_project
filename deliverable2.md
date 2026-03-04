1. Garbage Cleaning & Duplicate Removal

    What is being cleaned: I am cleaning JSON-like string blobs (e.g., genres, production_companies, spoken_languages) and API-specific artifacts like id and imdb_id which act as unique identifiers but offer no predictive power.

    `Adult` and `Status` are always constant

    The "Why" (7pt): Nested strings are "garbage" to a machine learning model because they are interpreted as flat text. A model cannot "see" that a movie is an "Action" film if that word is buried inside a 500-character string. Cleaning creates tidy data where each feature is a single, usable value.

    The "How": I am using the ast.literal_eval library in Python to convert strings into list/dictionary objects, then extracting the 'name' keys.

    Edge Case Handling: Some JSON strings are empty [] or malformed. I use try-except blocks within parsing functions to return NaN for malformed strings rather than crashing the script.

    The Result: Duplicate records based on the id column are removed to ensure the model doesn't overfit to specific blockbuster entries that may have been pulled multiple times via the API.

2. Handling Missing Values

    Why they are missing (7pt):

        Inherent Absence: Not every movie has a tagline or homepage.

        Unreleased Status: Obscure or future titles lack runtime or release_date.

        The "Zero" Problem (API Artifacts): In the TMDB API, missing financial data (budget and revenue) is typically returned as 0 rather than a null value. These are "False Zeros" that require filtering to avoid corrupting statistical analysis.
        

    Types of Missingness:

        MNAR (Missing Not at Random): belongs_to_collection is missing because the movie is simply not a sequel/franchise; the missingness is the data.

        MAR (Missing at Random): runtime might be missing for older films where records were not digitized.

    Handling Strategy:

        Categorical: Fill tagline and homepage with the string "None".

        Structural: Fill belongs_to_collection with "Standalone".

        Numerical: Use Median Imputation for runtime based on the movie's genre to avoid skewing the mean.

        Financial Filtering (Crucial):

        Row Deletion: Rows with budget == 0 or revenue == 0 are dropped. Because financial data is the primary target for many models, imputing a median budget would create artificial "averages" that dilute the signal of real blockbusters.

    The Impact: This prevents the deletion of nearly 80% of the dataset (specifically due to the collection column), while maintaining a representative distribution for numerical features.

3. Feature Engineering

    The "Why" (3pt): To turn raw metadata into predictive signals. A raw release_date is too granular; extracting release_month or release_quarter captures critical seasonal trends like "Summer Blockbusters" or "Oscar Season" releases.

    The Impact: Engineering a has_homepage binary feature and collection_count provides the model with indicators of marketing budget and franchise power—both are high-impact predictors for revenue.

4. Feature Redundancy & Constants

    `Adult` and `Status` are always constant

    The "Why" (4pt): API calls often return redundant fields like "Original Title" and "English Title," which are identical for most domestic films. Additionally, features like status might be "Released" for 99.9% of the rows (Quasi-constant), providing no information gain.

    Handling Strategy:

        Redundant: Drop original_title and backdrop_path.

        Quasi-Constant: Use a Variance Threshold; if a value is the same in >95% of rows, the column is dropped.

    The Impact: This reduces multi-collinearity, preventing the model from becoming over-complex or "confused" by variables that provide the same information.

5. Shape & Normalization

    Dataset Shape:

        Before: (4776,27)

        After: ≈(3901,12) (Refined selection of high-impact features).

Normalization Strategy: Z-Score (Standardization)

    Why: Features like runtime and popularity are on vastly different scales. Using Z-Score Normalization transforms these features to have a mean of 0 and a standard deviation of 1. This ensures that the model treats each feature with equal importance during training.

    Log Transformation for Target: Because revenue and budget follow a power-law distribution (most make little, few make billions), I apply a Log Transformation (y=log(x+1)).

    The Impact: Normalization speeds up model convergence and prevents features with larger raw numbers from dominating the model's weight updates. The log transform pulls extreme outliers inward, allowing the model to see the underlying relationship more clearly.