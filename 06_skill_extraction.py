"""
06_skill_extraction.py

Purpose:
- Extract and standardize skills from resume text
- Generate structured skill data
"""

import pandas as pd


INPUT_PATH = "data/cleaned/resume_skills_extracted.csv"
OUTPUT_PATH = "data/cleaned/final_resume_skills.csv"


# Skill categories

SKILL_CATEGORIES = {
    "Programming": [
        "Python",
        "Java",
        "C++",
        "JavaScript"
    ],

    "Data": [
        "SQL",
        "Excel",
        "Pandas",
        "NumPy",
        "Power BI",
        "Tableau",
        "Data Analysis",
        "Data Visualization"
    ],

    "AI_ML": [
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Scikit Learn"
    ],

    "Cloud": [
        "AWS",
        "Azure",
        "Docker"
    ]
}


def categorize_skills(skill_list):

    categories = []

    for category, skills in SKILL_CATEGORIES.items():

        for skill in skill_list:

            if skill in skills:
                categories.append(category)

    return list(set(categories))


print("Loading extracted skills...")

df = pd.read_csv(INPUT_PATH)


# Convert string list back to Python list

df["extracted_skills"] = df["extracted_skills"].apply(
    eval
)


# Add skill categories

df["skill_category"] = df["extracted_skills"].apply(
    categorize_skills
)


# Save result

df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("Skill categorization completed!")
print("Saved:", OUTPUT_PATH)


print("\nSample:")
print(df.head())