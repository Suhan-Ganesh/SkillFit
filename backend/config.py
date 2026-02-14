"""
Configuration module for the Market Alignment Engine.
Contains the hardcoded skill dictionary.
"""

# Hardcoded list of skills (technical and soft)
# All lowercase for case-insensitive matching
SKILLS = [
    # Technical Skills
    "python", "java", "c++", "javascript", "typescript", "html", "css", "sql",
    "nosql", "postgresql", "mongodb", "aws", "azure", "gcp", "docker",
    "kubernetes", "terraform", "linux", "git", "ci/cd", "machine learning",
    "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
    "scikit-learn", "pandas", "numpy", "matplotlib", "seaborn", "flask",
    "django", "fastapi", "react", "angular", "vue", "node.js", "next.js",
    "graphql", "rest api", "microservices", "system design", "agile", "scrum",
    "data analysis", "data visualization", "big data", "spark", "hadoop",
    
    # Soft Skills & General
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "adaptability", "time management", "collaboration",
    "mentoring", "presentation", "project management", "creativity"
]

# Dataset Configuration
DATASET_PATH = "job_postings.csv"  # Path to the LinkedIn dataset CSV
