"""
Data loading module for the Market Alignment Engine.
Handles loading and filtering of job posting data.
"""

import pandas as pd
import os
from config import DATASET_PATH

def load_and_filter_jobs(role_name: str, limit: int = 500) -> list:
    """
    Loads job postings from CSV, filters by role_name, and returns a list of descriptions.
    
    Args:
        role_name: The job role to filter for (case-insensitive substring match).
        limit: Maximum number of job descriptions to return.
        
    Returns:
        List of job description strings.
        
    Raises:
        FileNotFoundError: If the dataset file doesn't exist.
        ValueError: If required columns are missing.
    """
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

    try:
        # Load the dataset
        df = pd.read_csv(DATASET_PATH)
    except Exception as e:
         raise Exception(f"Failed to read CSV file: {e}")

    # Clean column names
    df.columns = [c.strip() for c in df.columns]

    # Check for required columns. 
    # LinkedIn Job Postings Dataset typically has 'job_title' and 'job_description'
    required_cols = {'job_title', 'job_description'}
    
    if not required_cols.issubset(df.columns):
         # distinct datasets might have 'title' instead of 'job_title'. check for that.
         if 'title' in df.columns and 'description' in df.columns:
             df.rename(columns={'title': 'job_title', 'description': 'job_description'}, inplace=True)
         else:
             raise ValueError(f"CSV missing required columns: {required_cols}")

    # Filter by role (case-insensitive)
    filtered_df = df[df['job_title'].str.contains(role_name, case=False, na=False)]

    if filtered_df.empty:
        return []

    # Limit to 500
    filtered_df = filtered_df.head(limit)

    # Return list of descriptions
    return filtered_df['job_description'].dropna().tolist()
